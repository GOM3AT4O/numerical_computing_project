import {
  Component,
  forwardRef,
  inject,
  input,
  OnChanges,
  SimpleChanges,
} from "@angular/core";
import {
  AbstractControl,
  ControlValueAccessor,
  FormArray,
  FormControl,
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  NonNullableFormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  Validator,
  ValidatorFn,
  Validators,
} from "@angular/forms";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { RangePipe } from "../../pipes/range.pipe";

@Component({
  selector: "app-equations",
  imports: [ReactiveFormsModule, AutoSizeInputDirective, RangePipe],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => EquationsComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => EquationsComponent),
      multi: true,
    },
  ],
  templateUrl: "./equations.component.html",
  styleUrl: "./equations.component.css",
})
export class EquationsComponent
  implements ControlValueAccessor, Validator, OnChanges
{
  private formBuilder = inject(NonNullableFormBuilder);

  equationCount = input<number>(3);

  numberValidator = Validators.pattern(/^[-+]?\d+(\.\d+)?$/);

  form = this.formBuilder.group({
    coefficients: this.formBuilder.array<FormArray<FormControl<string>>>([]),
    constants: this.formBuilder.array<FormControl<string>>([]),
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
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes["equationCount"]) {
      this.writeValue(this.form.value);
      this.onChange(this.form.value);
    }
  }

  writeValue(value: any): void {
    while (this.form.controls.coefficients.length < this.equationCount()) {
      const row = this.formBuilder.array<FormControl<string>>(
        Array.from({ length: this.equationCount() }, () =>
          this.formBuilder.control<string>("", this.numberValidator),
        ),
      );
      this.form.controls.coefficients.push(row);
    }

    while (this.form.controls.coefficients.length > this.equationCount()) {
      this.form.controls.coefficients.removeAt(
        this.form.controls.coefficients.length - 1,
      );
    }

    for (let i = 0; i < this.form.controls.coefficients.length; i++) {
      const row = this.form.controls.coefficients.at(i);
      while (row.length < this.equationCount()) {
        row.push(this.formBuilder.control<string>("", this.numberValidator));
      }

      while (row.length > this.equationCount()) {
        row.removeAt(row.length - 1);
      }
    }

    while (this.form.controls.constants.length < this.equationCount()) {
      this.form.controls.constants.push(
        this.formBuilder.control<string>("", this.numberValidator),
      );
    }

    while (this.form.controls.constants.length > this.equationCount()) {
      this.form.controls.constants.removeAt(
        this.form.controls.constants.length - 1,
      );
    }

    for (let i = 0; i < this.equationCount(); i++) {
      for (let j = 0; j < this.equationCount(); j++) {
        this.form.controls.coefficients
          .at(i)
          .at(j)
          .setValue(value?.coefficients?.[i]?.[j] ?? "", { emitEvent: false });
      }
      this.form.controls.constants
        .at(i)
        .setValue(value?.constants?.[i] ?? "", { emitEvent: false });
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
    }
  }

  validate(_: AbstractControl): ValidationErrors | null {
    return this.form.valid ? null : { equationsInvalid: true };
  }
}
