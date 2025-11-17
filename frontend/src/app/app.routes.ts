import { Routes } from "@angular/router";
import { EquationsSolverComponent } from "./components/equations-solver/equations-solver.component";

export const routes: Routes = [
  { path: "", redirectTo: "/equations-solver", pathMatch: "full" },
  {
    path: "equations-solver",
    component: EquationsSolverComponent,
    title: "System of Linear Equations Solver",
  },
];
