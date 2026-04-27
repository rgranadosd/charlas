package com.example.apim.guardrails;

import org.apache.axiom.om.OMAbstractFactory;
import org.apache.axiom.om.OMAttribute;
import org.apache.axiom.om.OMElement;
import org.apache.axiom.om.OMNode;
import org.apache.axiom.om.OMText;
import org.apache.axis2.AxisFault;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.synapse.MessageContext;
import org.apache.synapse.commons.json.JsonUtil;
import org.apache.synapse.core.axis2.Axis2MessageContext;
import org.apache.synapse.mediators.AbstractMediator;
import org.apache.synapse.transport.passthru.util.RelayUtils;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.node.TextNode;

import javax.xml.stream.XMLStreamException;
import java.io.IOException;
import java.util.Iterator;
import java.util.regex.Pattern;

public class InputSanitizationMediator extends AbstractMediator {

    private static final Log log = LogFactory.getLog(InputSanitizationMediator.class);
    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();
    private static final Pattern ESCAPED_INVISIBLE_UNICODE_PATTERN =
            Pattern.compile("(?i)\\\\u(?:200[b-f]|202[a-e]|206[0-4]|feff)");

    private String invisibleUnicodeRegex =
            "[\\u200B\\u200C\\u200D\\u200E\\u200F\\u202A-\\u202E\\u2060-\\u2064\\uFEFF]";

    private String dangerousOperatorsRegex =
            "&&|\\|\\||==|!=|>=|<=|<<|>>|;(?!\\s*$)|\\u0060[^\\u0060]*\\u0060|\\$\\([^)]*\\)";

    private String mode = "sanitize";

    @Override
    public boolean mediate(MessageContext synCtx) {
        org.apache.axis2.context.MessageContext axis2MessageContext =
                ((Axis2MessageContext) synCtx).getAxis2MessageContext();

        try {
            RelayUtils.buildMessage(axis2MessageContext);

            String effectiveMode = resolveProperty(synCtx, "mode", mode);
            if (!"sanitize".equalsIgnoreCase(effectiveMode)) {
                return true;
            }

            Pattern invisiblePattern = Pattern.compile(
                    resolveProperty(synCtx, "invisibleUnicodeRegex", invisibleUnicodeRegex));
            Pattern dangerousPattern = Pattern.compile(
                    resolveProperty(synCtx, "dangerousOperatorsRegex", dangerousOperatorsRegex));

            boolean changed;
            if (JsonUtil.hasAJsonPayload(axis2MessageContext)) {
                changed = sanitizeJson(axis2MessageContext, invisiblePattern, dangerousPattern);
            } else {
                changed = sanitizeXmlOrText(axis2MessageContext, invisiblePattern, dangerousPattern);
            }

            if (changed && log.isDebugEnabled()) {
                log.debug("InputSanitizationMediator sanitized request payload");
            }

            if (changed && log.isInfoEnabled()) {
                log.info("InputSanitizationMediator sanitized request payload"
                        + formatRequestContext(axis2MessageContext));
            }

            return true;
        } catch (IOException | XMLStreamException e) {
            handleException("InputSanitizationMediator failed to sanitize the request payload", e, synCtx);
            return false;
        }
    }

    private String formatRequestContext(org.apache.axis2.context.MessageContext axis2MessageContext) {
        StringBuilder context = new StringBuilder();
        appendContextValue(context, "messageId", axis2MessageContext.getMessageID());
        appendContextValue(context, "correlationId", axis2MessageContext.getProperty("correlation_id"));
        appendContextValue(context, "requestPath", axis2MessageContext.getProperty("REST_SUB_REQUEST_PATH"));
        return context.toString();
    }

    private void appendContextValue(StringBuilder context, String key, Object value) {
        if (value == null) {
            return;
        }
        context.append(context.length() == 0 ? " - " : ", ");
        context.append(key).append('=').append(value);
    }

    private boolean sanitizeJson(org.apache.axis2.context.MessageContext axis2MessageContext,
                                 Pattern invisiblePattern,
                                 Pattern dangerousPattern) throws AxisFault {
        String original = JsonUtil.jsonPayloadToString(axis2MessageContext);

        try {
            JsonNode rootNode = OBJECT_MAPPER.readTree(original);
            boolean changed = sanitizeJsonNode(rootNode, invisiblePattern, dangerousPattern);

            if (!changed) {
                return false;
            }

            String sanitized = OBJECT_MAPPER.writeValueAsString(rootNode);
            JsonUtil.getNewJsonPayload(axis2MessageContext, sanitized, true, true);
            JsonUtil.setContentType(axis2MessageContext);
            return true;
        } catch (IOException e) {
            throw AxisFault.makeFault(e);
        }
    }

    private boolean sanitizeJsonNode(JsonNode node,
                                     Pattern invisiblePattern,
                                     Pattern dangerousPattern) {
        if (node == null) {
            return false;
        }

        boolean changed = false;

        if (node instanceof ObjectNode) {
            ObjectNode objectNode = (ObjectNode) node;
            Iterator<String> fieldNames = objectNode.fieldNames();
            while (fieldNames.hasNext()) {
                String fieldName = fieldNames.next();
                JsonNode childNode = objectNode.get(fieldName);

                if (childNode instanceof TextNode) {
                    String originalText = childNode.asText();
                    String sanitizedText = sanitize(originalText, invisiblePattern, dangerousPattern);
                    if (!originalText.equals(sanitizedText)) {
                        objectNode.put(fieldName, sanitizedText);
                        changed = true;
                    }
                } else {
                    changed = sanitizeJsonNode(childNode, invisiblePattern, dangerousPattern) || changed;
                }
            }
            return changed;
        }

        if (node instanceof ArrayNode) {
            ArrayNode arrayNode = (ArrayNode) node;
            for (int index = 0; index < arrayNode.size(); index++) {
                JsonNode childNode = arrayNode.get(index);

                if (childNode instanceof TextNode) {
                    String originalText = childNode.asText();
                    String sanitizedText = sanitize(originalText, invisiblePattern, dangerousPattern);
                    if (!originalText.equals(sanitizedText)) {
                        arrayNode.set(index, TextNode.valueOf(sanitizedText));
                        changed = true;
                    }
                } else {
                    changed = sanitizeJsonNode(childNode, invisiblePattern, dangerousPattern) || changed;
                }
            }
        }

        return changed;
    }

    private boolean sanitizeXmlOrText(org.apache.axis2.context.MessageContext axis2MessageContext,
                                      Pattern invisiblePattern,
                                      Pattern dangerousPattern) {
        if (axis2MessageContext.getEnvelope() == null || axis2MessageContext.getEnvelope().getBody() == null) {
            return false;
        }

        return sanitizeNode(axis2MessageContext.getEnvelope().getBody(), invisiblePattern, dangerousPattern);
    }

    private boolean sanitizeNode(OMNode node, Pattern invisiblePattern, Pattern dangerousPattern) {
        boolean changed = false;

        if (node instanceof OMText) {
            OMText textNode = (OMText) node;
            String original = textNode.getText();
            String sanitized = sanitize(original, invisiblePattern, dangerousPattern);
            if (!original.equals(sanitized)) {
                OMText replacement = OMAbstractFactory.getOMFactory().createOMText(sanitized);
                textNode.insertSiblingAfter(replacement);
                textNode.detach();
                return true;
            }
            return false;
        }

        if (node instanceof OMElement) {
            OMElement element = (OMElement) node;

            for (Iterator<?> iterator = element.getAllAttributes(); iterator.hasNext(); ) {
                OMAttribute attribute = (OMAttribute) iterator.next();
                String original = attribute.getAttributeValue();
                String sanitized = sanitize(original, invisiblePattern, dangerousPattern);
                if (!original.equals(sanitized)) {
                    attribute.setAttributeValue(sanitized);
                    changed = true;
                }
            }

            for (Iterator<?> iterator = element.getChildren(); iterator.hasNext(); ) {
                OMNode child = (OMNode) iterator.next();
                changed = sanitizeNode(child, invisiblePattern, dangerousPattern) || changed;
            }
        }

        return changed;
    }

    private String sanitize(String input, Pattern invisiblePattern, Pattern dangerousPattern) {
        if (input == null || input.isEmpty()) {
            return input;
        }

        String withoutEscapedInvisible = ESCAPED_INVISIBLE_UNICODE_PATTERN.matcher(input).replaceAll("");
        String withoutInvisible = invisiblePattern.matcher(withoutEscapedInvisible).replaceAll("");
        return dangerousPattern.matcher(withoutInvisible).replaceAll(" ");
    }

    private String resolveProperty(MessageContext synCtx, String propertyName, String fallback) {
        Object value = synCtx.getProperty(propertyName);
        if (value instanceof String && !((String) value).isEmpty()) {
            return (String) value;
        }
        return fallback;
    }

    public void setInvisibleUnicodeRegex(String invisibleUnicodeRegex) {
        this.invisibleUnicodeRegex = invisibleUnicodeRegex;
    }

    public void setDangerousOperatorsRegex(String dangerousOperatorsRegex) {
        this.dangerousOperatorsRegex = dangerousOperatorsRegex;
    }

    public void setMode(String mode) {
        this.mode = mode;
    }
}