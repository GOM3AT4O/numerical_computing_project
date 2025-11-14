import {
  Component,
  forwardRef,
  inject,
  input,
  OnChanges,
  SimpleChanges,
} from "@angular/core";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { RangePipe } from "../../pipes/range.pipe";
import {
  AbstractControl,
  ControlValueAccessor,
  FormBuilder,
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule,
  ValidationErrors,
  Validator,
  Validators,
} from "@angular/forms";

@Component({
  selector: "app-iteration-parameters",
  imports: [ReactiveFormsModule, AutoSizeInputDirective, RangePipe],
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
export class IterationParametersComponent
  implements ControlValueAccessor, Validator, OnChanges
{
  private formBuilder = inject(FormBuilder);

  equationCount = input<number>(3);

  numberValidator = Validators.pattern(/^[-+]?\d+(\.\d+)?$/);

  stoppingConditions = [
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
  ];

  form = this.formBuilder.group({
    initialGuess: this.formBuilder.nonNullable.array<string>([]),
    stoppingCondition: [this.stoppingConditions[0].value, Validators.required],
    numberOfIterations: [
      { value: "", disabled: false },
      [Validators.required, Validators.pattern(/^[1-9]\d*$/)],
    ],
    absoluteRelativeError: [
      { value: "", disabled: true },
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
  });

  private onChange: (_: any) => void = () => {};
  private onTouched: () => void = () => {};

  ngOnInit() {
    this.form.valueChanges.subscribe((value) => {
      this.onChange(value);
      this.onTouched();
    });

    setTimeout(() => {
      this.onChange(this.form.value);
    });

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

  ngOnChanges(changes: SimpleChanges): void {
    if (changes["equationCount"]) {
      this.writeValue(this.form.value);
      this.onChange(this.form.value);
    }
  }

  writeValue(value: any): void {
    if (value) {
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

    while (this.form.controls.initialGuess.length < this.equationCount()) {
      this.form.controls.initialGuess.push(
        this.formBuilder.nonNullable.control<string>("", this.numberValidator),
      );
    }

    while (this.form.controls.initialGuess.length > this.equationCount()) {
      this.form.controls.initialGuess.removeAt(
        this.form.controls.initialGuess.length - 1,
      );
    }

    for (let i = 0; i < this.equationCount(); i++) {
      this.form.controls.initialGuess
        .at(i)
        .setValue(value?.initialGuess?.[i] ?? "", { emitEvent: false });
    }
  }

  registerOnChange(fn: (_: any) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  setDisabledState?(isDisabled: boolean): void {
    if (isDisabled) {
      this.form.disable();
    } else {
      this.form.enable();

      for (const condition of this.stoppingConditions) {
        if (condition.value !== this.form.get("stoppingCondition")?.value) {
          this.form.get(condition.controlName)?.disable();
        }
      }
    }
  }

  validate(_: AbstractControl): ValidationErrors | null {
    return this.form.valid ? null : { parametersInvalid: true };
  }
}
