import { Component, forwardRef, inject } from "@angular/core";
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
  selector: "app-lu-parameters",
  imports: [ReactiveFormsModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => LUParametersComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => LUParametersComponent),
      multi: true,
    },
  ],
  templateUrl: "./lu-parameters.component.html",
  styleUrl: "./lu-parameters.component.css",
})
export class LUParametersComponent implements ControlValueAccessor, Validator {
  private formBuilder = inject(FormBuilder);

  formats = [
    { label: "Doolittle Form", value: "doolittle" },
    { label: "Crout Form", value: "crout" },
    { label: "Cholesky Form", value: "cholesky" },
  ];

  form = this.formBuilder.group({
    format: [this.formats[0].value, Validators.required],
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

  writeValue(value: any): void {
    if (value) {
      if (value.format) {
        this.form.controls.format.setValue(value.format, { emitEvent: false });
      }
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
    return this.form.valid ? null : { parametersInvalid: true };
  }
}
