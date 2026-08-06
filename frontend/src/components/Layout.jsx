import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

function Layout() {
  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        background: "#f4f6f9",
      }}
    >
      <Sidebar />

      <div
        style={{
          flex: 1,
          marginLeft: "250px",
          display: "flex",
          flexDirection: "column",
          minHeight: "100vh",
        }}
      >
        <Navbar />

        <main
          style={{
            flex: 1,
            marginTop: "70px",
            padding: "24px",
            overflowX: "auto",
          }}
        >
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default Layout;
