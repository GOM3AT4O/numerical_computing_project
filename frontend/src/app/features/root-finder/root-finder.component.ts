import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  inject,
  signal,
  viewChild,
} from "@angular/core";
import {
  ReactiveFormsModule,
  FormBuilder,
  Validators,
  AbstractControl,
  ValidationErrors,
} from "@angular/forms";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { parse, SymbolNode } from "mathjs";
import { PlotComponent } from "./components/plot/plot.component";
import { ParametersComponent } from "./components/parameters/parameters.component";
import { FindRootResponse } from "./models/find-root-response";
import { IntervalParametersComponent } from "./components/parameters/interval-parameters/interval-parameters.component";
import { OneGuessParametersComponent } from "./components/parameters/one-guess-parameters/one-guess-parameters.component";
import { TwoGuessesParametersComponent } from "./components/parameters/two-guesses-parameters/two-guesses-parameters.component";

@Component({
  selector: "app-root-finder",
  imports: [
    ReactiveFormsModule,
    AutoSizeInputDirective,
    PlotComponent,
    IntervalParametersComponent,
    OneGuessParametersComponent,
    TwoGuessesParametersComponent,
  ],
  templateUrl: "./root-finder.component.html",
  styleUrl: "./root-finder.component.css",
})
export class RootFinderComponent {
  private formBuilder = inject(FormBuilder);
  private changeDetectorRef = inject(ChangeDetectorRef);

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

  methodLabels = Object.fromEntries(
    this.methods.map(({ label, value }) => [value, label] as const),
  );

  form = this.formBuilder.group({
    function: ["", [Validators.required, this.functionValidator]],
    method: [
      this.methods[0].value as (typeof this.methods)[number]["value"],
      Validators.required,
    ],
    precision: ["", [Validators.pattern(/^[1-9]\d*$/)]],
    numberOfIterations: [
      "",
      [Validators.required, Validators.pattern(/^[1-9]\d*$/)],
    ],
    absoluteRelativeError: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
    parameters: [null as any],
  });

  functions: { [k: string]: string } = {};

  parameters = viewChild<ParametersComponent>("parameters");
  parametersElement = viewChild("parameters", { read: ElementRef });

  response = signal<FindRootResponse | null>(null);

  resultElement = viewChild<ElementRef<HTMLDivElement>>("result");

  ngOnInit() {
    this.form.get("function")?.valueChanges.subscribe((f) => {
      if (this.form.get("function")?.valid) {
        if (this.form.get("method")?.value === "fixed-point") {
          this.functions = { ...this.functions, ["g(x)"]: f! };
        } else {
          this.functions = { ...this.functions, ["f(x)"]: f! };
        }
      }
    });

    this.form.get("method")?.valueChanges.subscribe((method) => {
      if (method === "fixed-point") {
        this.functions = { ["g(x)"]: this.functions["f(x)"], ["x"]: "x" };
      } else if (!this.functions["f(x)"]) {
        this.functions = { ["f(x)"]: this.functions["g(x)"] };
      }

      this.form.setControl("parameters", this.formBuilder.control(null));
      this.changeDetectorRef.detectChanges();
      // scroll to show the parameters section
      setTimeout(() => {
        this.parametersElement()?.nativeElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });
    });
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
