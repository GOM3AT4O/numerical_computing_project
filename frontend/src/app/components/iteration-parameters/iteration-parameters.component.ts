import { Component, forwardRef, input } from "@angular/core";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { RangePipe } from "../../pipes/range.pipe";
import {
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { MatrixComponent } from "../matrix/matrix.component";
import { ParametersComponent } from "../parameters/parameters.component";
import { IterationParameters } from "../../models/solve-equations-request";

@Component({
  selector: "app-iteration-parameters",
  imports: [
    ReactiveFormsModule,
    AutoSizeInputDirective,
    RangePipe,
    MatrixComponent,
  ],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => IterationParametersComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => IterationParametersComponent),
      multi: true,
    },
  ],
  templateUrl: "./iteration-parameters.component.html",
  styleUrl: "./iteration-parameters.component.css",
})
export class IterationParametersComponent extends ParametersComponent {
  equationCount = input<number>(3);

  numberValidator = Validators.pattern(/^[-+]?\d+(\.\d+)?$/);

  readonly stoppingConditions = [
    {
      label: "Number of Iterations",
      value: "number-of-iterations",
      controlName: "numberOfIterations",
    },
    {
      label: "Absolute Relative Error",
      value: "absolute-relative-error",
      controlName: "absoluteRelativeError",
    },
  ] as const;

  form = this.formBuilder.group({
    initialGuess: [[] as string[][], Validators.required],
    stoppingCondition: [
      this.stoppingConditions[0]
        .value as (typeof this.stoppingConditions)[number]["value"],
      Validators.required,
    ],
    numberOfIterations: [
      { value: "", disabled: false },
      [Validators.required, Validators.pattern(/^[1-9]\d*$/)],
    ],
    absoluteRelativeError: [
      { value: "", disabled: true },
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
  });

  override get parameters(): IterationParameters {
    const value = this.form.value!;
    console.log(value);
    const initialGuess = value.initialGuess!.map((value: string[]) =>
      value[0].trim() === "" ? "0" : value[0],
    );

    switch (value.stoppingCondition!) {
      case "number-of-iterations":
        return {
          initialGuess,
          stoppingCondition: value.stoppingCondition!,
          numberOfIterations: parseInt(value.numberOfIterations!, 10),
        };
      case "absolute-relative-error":
        return {
          initialGuess,
          stoppingCondition: value.stoppingCondition!,
          absoluteRelativeError: value.absoluteRelativeError!,
        };
    }
  }

  override ngOnInit() {
    super.ngOnInit();

    this.form.get("stoppingCondition")?.valueChanges.subscribe((value) => {
      for (const condition of this.stoppingConditions) {
        if (condition.value === value) {
          this.form.get(condition.controlName)?.enable();
        } else {
          this.form.get(condition.controlName)?.disable();
        }
      }
    });
  }

  writeValue(value: any): void {
    if (value) {
      if (value.initialGuess) {
        this.form
          .get("initialGuess")
          ?.setValue(value.initialGuess, { emitEvent: false });
      }
      if (value.stoppingCondition) {
        this.form
          .get("stoppingCondition")
          ?.setValue(value.stoppingCondition, { emitEvent: false });
      }
      for (const condition of this.stoppingConditions) {
        if (value[condition.controlName]) {
          this.form
            .get(condition.controlName)
            ?.setValue(value[condition.controlName], {
              emitEvent: false,
            });
        }
      }
    }
  }

  override setDisabledState?(isDisabled: boolean): void {
    super.setDisabledState?.(isDisabled);

    if (!isDisabled) {
      for (const condition of this.stoppingConditions) {
        if (condition.value !== this.form.get("stoppingCondition")?.value) {
          this.form.get(condition.controlName)?.disable();
        }
      }
    }
  }
}
