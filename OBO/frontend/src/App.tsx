import { useEffect } from "react";

import { DashboardPage } from "./pages/DashboardPage";

export default function App() {
  useEffect(() => {
    document.documentElement.dataset.theme = "dark";
  }, []);

  return <DashboardPage />;
}
