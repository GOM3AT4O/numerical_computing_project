import { Routes } from "@angular/router";
import { EquationsSolverComponent } from "./features/equations-solver/equations-solver.component";
import { RootFinderComponent } from "./features/root-finder/root-finder.component";

export const routes: Routes = [
  { path: "", redirectTo: "/equations-solver", pathMatch: "full" },
  {
    path: "equations-solver",
    component: EquationsSolverComponent,
    title: "System of Linear Equations Solver",
  },
  {
    path: "root-finder",
    component: RootFinderComponent,
    title: "Root Finder",
  },
];
