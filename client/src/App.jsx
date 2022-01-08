import logo from "./logo.svg";
import "./App.css";
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
} from "react-router-dom";
import Login from "./views/Auth/Login";
import Register from "./views/Auth/Register";
import Databases from "./views/Dashboard/Databases";
import Tables from "./views/Dashboard/Tables";
import TableOverview from "./views/Analysis/TableOverview";
import { SwitchThemeButton } from "./components/Util/SwitchTheme";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route exact path="/">
            <Redirect to="/dashboard" />
          </Route>
          <Route path="/login">
            <Login />
          </Route>
          <Route path="/register">
            <Register />
          </Route>
          <Route path="/dashboard">
            <Databases />
          </Route>
          <Route exact path="/database/:databaseID">
            <Tables />
          </Route>
          <Route exact path="/table/:tableID">
            <TableOverview />
          </Route>
        </Switch>
      </Router>
      <SwitchThemeButton />

    </div>
  );
}

export default App;
