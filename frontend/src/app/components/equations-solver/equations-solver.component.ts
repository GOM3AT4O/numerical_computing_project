import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  inject,
  signal,
  viewChild,
} from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";
import { EquationsComponent } from "../equations/equations.component";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { LUParametersComponent } from "../parameters/lu-parameters/lu-parameters.component";
import { IterationParametersComponent } from "../parameters/iteration-parameters/iteration-parameters.component";
import { EquationsSolverService } from "../../services/equations-solver.service";
import { SolveEquationsRequest } from "../../models/solve-equations-request";
import { SolveEquationsResponse } from "../../models/solve-equations-response";
import { ParametersComponent } from "../parameters/parameters.component";
import { StepComponent } from "../step/step.component";
import { EliminationParametersComponent } from "../parameters/elimination-parameters/elimination-parameters.component";

@Component({
  selector: "app-equations-solver",
  imports: [
    ReactiveFormsModule,
    AutoSizeInputDirective,
    EquationsComponent,
    LUParametersComponent,
    IterationParametersComponent,
    EliminationParametersComponent,
    StepComponent,
  ],
  templateUrl: "./equations-solver.component.html",
  styleUrl: "./equations-solver.component.css",
})
export class EquationsSolverComponent {
  private equationSolverService = inject(EquationsSolverService);
  private formBuilder = inject(FormBuilder);
  private changeDetectorRef = inject(ChangeDetectorRef);

  equationCount = 3;

  readonly methods = [
    { label: "Gauss Elimination", value: "gauss-elimination" },
    { label: "Gauss-Jordan Elimination", value: "gauss-jordan-elimination" },
    { label: "LU Decomposition", value: "lu-decomposition" },
    { label: "Jacobi Iteration", value: "jacobi-iteration" },
    { label: "Gauss-Seidel Iteration", value: "gauss-seidel-iteration" },
  ] as const;

  form = this.formBuilder.group({
    equationCount: [
      this.equationCount.toString(),
      [Validators.required, Validators.pattern(/^[1-9]\d*$/)],
    ],
    equations: [
      { coefficients: [[]] as string[][], constants: [] as string[] },
      Validators.required,
    ],
    method: [
      this.methods[0].value as (typeof this.methods)[number]["value"],
      Validators.required,
    ],
    precision: ["", [Validators.pattern(/^[1-9]\d*$/)]],
    parameters: [null as any],
  });

  parameters = viewChild<ParametersComponent>("parameters");
  parametersElement = viewChild("parameters", { read: ElementRef });

  showSteps = signal<boolean>(false);
  response = signal<SolveEquationsResponse | null>(null);
  errorResponse = signal<string | null>(null);

  resultElement = viewChild<ElementRef<HTMLDivElement>>("result");

  stepsElement = viewChild<ElementRef<HTMLDivElement>>("steps");

  ngOnInit() {
    this.form.get("equationCount")?.valueChanges.subscribe((count) => {
      if (this.form.get("equationCount")?.valid) {
        this.equationCount = parseInt(count!, 10);
        this.changeDetectorRef.detectChanges();
      }
    });

    this.form.get("method")?.valueChanges.subscribe(() => {
      this.form.setControl("parameters", this.formBuilder.control(null));
      this.changeDetectorRef.detectChanges();
      setTimeout(() => {
        this.parametersElement()?.nativeElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });
    });

    this.form.get("equations")?.setValue({
      coefficients: [
        [2, -1, 1].map(String),
        [3, 3, 9].map(String),
        [3, 3, 5].map(String),
      ],
      constants: [0, 0, 0].map(String),
    });
  }

  clear() {
    this.form.get("equations")?.setValue({
      coefficients: Array.from({ length: this.equationCount }, () =>
        Array.from({ length: this.equationCount }, () => ""),
      ),
      constants: Array.from({ length: this.equationCount }, () => ""),
    });
  }

  solve() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.parameters()?.form.markAllAsTouched();
      return;
    }

    const value = this.form.value;

    const request: SolveEquationsRequest = {
      equations: {
        coefficients: value.equations!.coefficients.map((row: string[]) =>
          row.map((value: string) => (value.trim() === "" ? "0" : value)),
        ),
        constants: value.equations!.constants.map((value: string) =>
          value.trim() === "" ? "0" : value,
        ),
      },
      method: value.method!,
      parameters: this.parameters()?.parameters as any,
      precision: isNaN(parseInt(value.precision!, 10))
        ? undefined
        : parseInt(value.precision!, 10),
    };

    this.equationSolverService.solveEquations(request).subscribe((response) => {
      this.showSteps.set(false);
      this.response.set(response);
      this.changeDetectorRef.detectChanges();
      setTimeout(() => {
        this.resultElement()?.nativeElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });
    });
  }

  toggleShowSteps() {
    this.showSteps.update((value) => !value);
    if (this.showSteps()) {
      this.changeDetectorRef.detectChanges();
      setTimeout(() => {
        this.stepsElement()?.nativeElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      });
    }
  }
}
