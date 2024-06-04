import { Route, Routes } from "react-router-dom";
import "./App.css";
import Profile from "./pages/Profile";
import Search from "./pages/Search";
import Service from "./pages/Service";

function App() {
  return (
    <main>
      <Routes>
        <Route path="/">
          <Route index element={<Search />} />
          <Route path="profile/:vendorId" element={<Profile />} />
          <Route path="service/:serviceId" element={<Service />} />
        </Route>
      </Routes>
    </main>
  );
}

export default App;
