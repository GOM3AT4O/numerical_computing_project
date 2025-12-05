import { Component, inject } from "@angular/core";
import {
  ReactiveFormsModule,
  FormBuilder,
  Validators,
  AbstractControl,
  ValidationErrors,
} from "@angular/forms";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { compile, EvalFunction, parse, SymbolNode } from "mathjs";
import { PlotlyComponent } from "angular-plotly.js";
import { PlotRelayoutEvent } from "plotly.js-dist-min";

@Component({
  selector: "app-root-finder",
  imports: [ReactiveFormsModule, AutoSizeInputDirective, PlotlyComponent],
  templateUrl: "./root-finder.component.html",
  styleUrl: "./root-finder.component.css",
})
export class RootFinderComponent {
  private formBuilder = inject(FormBuilder);

  readonly allowedSymbols: string[] = [
    "e",
    "pi",
    "sqrt",
    "cbrt",
    "sin",
    "cos",
    "tan",
    "csc",
    "sec",
    "cot",
    "asin",
    "acos",
    "atan",
    "acsc",
    "asec",
    "acot",
    "log",
    "ln",
    "exp",
  ] as const;

  readonly functionValidator = (
    control: AbstractControl,
  ): ValidationErrors | null => {
    if (!control.value) {
      return null;
    }

    try {
      const node = parse(control.value);
      const variables = node
        .filter((n) => n.type === "SymbolNode")
        .map((n) => (n as SymbolNode).name)
        .filter((n) => !this.allowedSymbols.includes(n));

      if (variables.length !== 0 && variables.some((v) => v !== "x")) {
        return { invalidFunction: true };
      }

      return null;
    } catch {
      return { invalidFunction: true };
    }
  };

  readonly methods = [
    { label: "Bisection", value: "bisection" },
    { label: "False-Position", value: "false-position" },
    { label: "Fixed-Point", value: "fixed-point" },
    { label: "Newton-Raphson", value: "newton-raphson" },
    { label: "Modified Newton-Raphson", value: "modified-newton-raphson" },
    { label: "Secant", value: "secant" },
  ] as const;

  form = this.formBuilder.group({
    function: ["", [Validators.required, this.functionValidator]],
    method: [
      this.methods[0].value as (typeof this.methods)[number]["value"],
      Validators.required,
    ],
    precision: ["", [Validators.pattern(/^[1-9]\d*$/)]],
    parameters: [null as any],
  });

  expression: EvalFunction | null = null;

  minX = -10;
  maxX = 10;

  graph = {
    data: [
      {
        x: [] as number[],
        y: [] as number[],
        type: "scatter",
        mode: "lines",
        name: "f(x)",
      },
    ],
    layout: {
      dragmode: "pan",
      margin: { l: 40, r: 40, t: 40, b: 40 },
      xaxis: { range: [this.minX, this.maxX], exponentformat: "power" },
      yaxis: { range: [this.minX, this.maxX], exponentformat: "power" },
      width: 400,
      height: 350,
      title: "A Fancy Plot",
    },
  };

  plot() {
    const numberOfPoints = 200;
    const step = (this.maxX - this.minX) / (numberOfPoints - 1);
    const x = Array.from(
      { length: numberOfPoints },
      (_, i) => this.minX + i * step,
    );
    const y = x.map((x) => this.expression!.evaluate({ x }));

    this.graph.data[0].x = x;
    this.graph.data[0].y = y;
  }

  ngOnInit() {
    this.form.get("function")?.valueChanges.subscribe((f) => {
      if (this.form.get("function")?.invalid) {
        return;
      }

      this.expression = compile(f!);
      this.plot();
    });
  }

  onRelayout(event: any) {
    if (
      event["xaxis.range[0]"] !== undefined &&
      event["xaxis.range[1]"] !== undefined
    ) {
      this.minX = event["xaxis.range[0]"] as number;
      this.maxX = event["xaxis.range[1]"] as number;
      this.plot();
    }
  }

  solve() {
    // check if the form is valid, otherwise mark all fields as touched to show validation errors
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const value = this.form.value;

    console.log(value);
  }
}
