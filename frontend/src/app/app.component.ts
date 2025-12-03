import { Component, inject } from "@angular/core";
import {
  Router,
  RouterLink,
  RouterLinkActive,
  RouterOutlet,
  NavigationEnd,
} from "@angular/router";
import { filter } from "rxjs";

@Component({
  selector: "app-root",
  imports: [RouterOutlet, RouterLink],
  templateUrl: "./app.component.html",
  styleUrl: "./app.component.css",
})
export class AppComponent {
  private router = inject(Router);

  tabs = [
    { label: "Equations Solver", path: "/equations-solver" },
    { label: "Root Finder", path: "/root-finder" },
  ];

  activeTabIndex = 0;
  slideDirection: "slide-left" | "slide-right" = "slide-left";

  ngOnInit(): void {
    this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe((event: NavigationEnd) => {
        const index = this.tabs.findIndex(
          (tab) => tab.path === event.urlAfterRedirects,
        );
        this.slideDirection =
          index > this.activeTabIndex ? "slide-right" : "slide-left";
        this.activeTabIndex = index;
      });
  }
}
