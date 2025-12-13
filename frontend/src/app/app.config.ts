import {
  ApplicationConfig,
  importProvidersFrom,
  provideBrowserGlobalErrorListeners,
  provideZoneChangeDetection,
} from "@angular/core";
import {
  ActivatedRouteSnapshot,
  provideRouter,
  withViewTransitions,
} from "@angular/router";

import { routes } from "./app.routes";
import { provideHttpClient } from "@angular/common/http";
import * as PlotlyJS from "plotly.js-dist-min";
import { PlotlyModule } from "angular-plotly.js";

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(
      routes,
      withViewTransitions({
        onViewTransitionCreated: ({ transition, from, to }) => {
          const getOrder = (
            snapshot: ActivatedRouteSnapshot,
          ): number | undefined => {
            return (snapshot.firstChild?.data as { order: number | undefined })
              ?.order;
          };

          const fromOrder = getOrder(from);
          const toOrder = getOrder(to);

          if (
            fromOrder === undefined ||
            toOrder === undefined ||
            fromOrder === toOrder
          )
            return;

          let directionClass = "";
          if (toOrder > fromOrder) {
            directionClass = "slide-left";
          } else if (toOrder < fromOrder) {
            directionClass = "slide-right";
          }

          if (directionClass) {
            document.documentElement.classList.add(directionClass);
            transition.finished.finally(() => {
              document.documentElement.classList.remove(
                "slide-right",
                "slide-left",
              );
            });
          }
        },
      }),
    ),
    provideHttpClient(),
    importProvidersFrom(PlotlyModule.forRoot(PlotlyJS)),
  ],
};
