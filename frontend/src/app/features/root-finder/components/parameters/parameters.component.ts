import { Directive, inject } from "@angular/core";
import {
  AbstractControl,
  ControlValueAccessor,
  FormBuilder,
  ValidationErrors,
  Validator,
} from "@angular/forms";

@Directive()
export abstract class ParametersComponent
  implements ControlValueAccessor, Validator
{
  protected formBuilder = inject(FormBuilder);

  abstract get form(): any;

  abstract get parameters(): { [key: string]: any };

  abstract writeValue(obj: any): void;

  private onChange: (_: any) => void = () => {};
  private onTouched: () => void = () => {};

  ngOnInit() {
    this.form.valueChanges.subscribe((value: any) => {
      this.onChange(value);
      this.onTouched();
    });

    setTimeout(() => {
      this.onChange(this.form.value);
    });
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
