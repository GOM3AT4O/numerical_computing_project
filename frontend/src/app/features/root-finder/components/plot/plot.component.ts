import { Component, input, OnChanges, SimpleChanges } from "@angular/core";
import { all, create, EvalFunction } from "mathjs";
import { PlotlyComponent } from "angular-plotly.js";
import { PlotRelayoutEvent } from "plotly.js-dist-min";

const math = create(all, { predictable: true });

@Component({
  selector: "app-plot",
  imports: [PlotlyComponent],
  templateUrl: "./plot.component.html",
  styleUrl: "./plot.component.css",
})
export class PlotComponent implements OnChanges {
  functions = input<{ [key: string]: string }>({});
  compiledFunctions: { [key: string]: EvalFunction } = {};

  minX = -10;
  maxX = 10;

  numberOfPoints = 1000;

  data: any[] = [];

  layout = {
    dragmode: "pan",
    margin: { l: 30, r: 30, t: 30, b: 30 },
    xaxis: { range: [this.minX, this.maxX], exponentformat: "power" },
    yaxis: { range: [this.minX, this.maxX], exponentformat: "power" },
    width: 400,
    height: 350,
    colorway: ["#2b7fff", "#fb2c36", "#00c951", "#efb100"],
    showlegend: false,
  };

  config = {
    displaylogo: false,
    modeBarButtonsToRemove: ["toImage"],
  };

  ngOnChanges(changes: SimpleChanges): void {
    if (changes["functions"]) {
      this.compileFunctions();
      this.generateData();
    }
  }

  compileFunctions() {
    this.compiledFunctions = Object.fromEntries(
      Object.entries(this.functions())
        .filter(([_, v]) => v)
        .map(([k, v]) => [k, math.compile(v)]),
    );
  }

  generateData() {
    const step = (this.maxX - this.minX) / (this.numberOfPoints - 1);
    const x = Array.from(
      { length: this.numberOfPoints },
      (_, i) => this.minX + i * step,
    );
    this.data = Object.entries(this.compiledFunctions).map(([k, v]) => ({
      x,
      y: x.map((x) => v.evaluate({ x })),
      type: "scatter",
      mode: "lines",
      name: k,
    }));
  }

  onRelayout(event: PlotRelayoutEvent) {
    if (
      event["xaxis.range[0]"] !== undefined &&
      event["xaxis.range[1]"] !== undefined
    ) {
      this.minX = event["xaxis.range[0]"] as number;
      this.maxX = event["xaxis.range[1]"] as number;
      this.generateData();
    }
  }
}
