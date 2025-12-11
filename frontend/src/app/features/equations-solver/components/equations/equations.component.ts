import {
  Component,
  ElementRef,
  forwardRef,
  inject,
  input,
  OnChanges,
  SimpleChanges,
  viewChildren,
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
  Validators,
} from "@angular/forms";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { RangePipe } from "../../../../shared/pipes/range.pipe";

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

  inputs = viewChildren<ElementRef<HTMLInputElement>>("input");

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
      // update the equations to match the new equation count
      this.writeValue(this.form.value);
      this.onChange(this.form.value);
    }
  }

  writeValue(value: any): void {
    // add rows to the coeffiecients matrix until it matches the equation count
    while (this.form.controls.coefficients.length < this.equationCount()) {
      const row = this.formBuilder.array<FormControl<string>>(
        Array.from({ length: this.equationCount() }, () =>
          this.formBuilder.control<string>("", this.numberValidator),
        ),
      );
      this.form.controls.coefficients.push(row);
    }

    // remove rows from the coeffiecients matrix until it matches the equation count
    while (this.form.controls.coefficients.length > this.equationCount()) {
      this.form.controls.coefficients.removeAt(
        this.form.controls.coefficients.length - 1,
      );
    }

    for (let i = 0; i < this.form.controls.coefficients.length; i++) {
      const row = this.form.controls.coefficients.at(i);
      // add columns to the coeffiecients matrix row until it matches the equation count
      while (row.length < this.equationCount()) {
        row.push(this.formBuilder.control<string>("", this.numberValidator));
      }

      // remove columns from the coeffiecients matrix row until it matches the equation count
      while (row.length > this.equationCount()) {
        row.removeAt(row.length - 1);
      }
    }

    // add constants until it matches the equation count
    while (this.form.controls.constants.length < this.equationCount()) {
      this.form.controls.constants.push(
        this.formBuilder.control<string>("", this.numberValidator),
      );
    }

    // remove constants until it matches the equation count
    while (this.form.controls.constants.length > this.equationCount()) {
      this.form.controls.constants.removeAt(
        this.form.controls.constants.length - 1,
      );
    }

    // set the values of the coeffiecients matrix and constants vector
    for (let i = 0; i < this.equationCount(); i++) {
      for (let j = 0; j < this.equationCount(); j++) {
        this.form.controls.coefficients
          .at(i)
          .at(j)
          .setValue(value?.coefficients?.[i]?.[j] ?? "");
      }
      this.form.controls.constants.at(i).setValue(value?.constants?.[i] ?? "");
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

  onKeyDown(i: number, j: number, event: KeyboardEvent) {
    const input =
      this.inputs()[i * (this.equationCount() + 1) + j].nativeElement;

    // navigate inputs based on arrow key pressed, if possible
    switch (event.key) {
      case "ArrowUp":
        i = i > 0 ? i - 1 : i;
        break;
      case "ArrowDown":
        i = i + 1 < this.equationCount() ? i + 1 : i;
        break;
      case "ArrowLeft":
        if (input.value.length !== 0 && input.selectionStart !== 0) {
          return;
        }
        // if at the first input in a row, move to the last input of the previous row
        if (j > 0) {
          j--;
        } else if (i > 0) {
          i--;
          j = this.equationCount() - 1;
        }
        break;
      case "ArrowRight":
        if (
          input.value.length !== 0 &&
          input.selectionStart !== input.value.length
        ) {
          return;
        }
        // if at the last input in a row, move to the first input of the next row
        if (j < this.equationCount()) {
          j++;
        } else if (i < this.equationCount() - 1) {
          i++;
          j = 0;
        }
        break;
      default:
        return;
    }

    event.preventDefault();
    // set focus to the new input
    this.inputs()[i * (this.equationCount() + 1) + j].nativeElement.focus();
  }

  // swap equations at index i and i-1, effictively moving equation i up
  moveEquationUp(i: number) {
    if (i === 0) return;

    const temporaryCoefficients = this.form.controls.coefficients.at(i).value;
    const temporaryConstant = this.form.controls.constants.at(i).value;

    this.form.controls.coefficients
      .at(i)
      .setValue(this.form.controls.coefficients.at(i - 1).value);
    this.form.controls.constants
      .at(i)
      .setValue(this.form.controls.constants.at(i - 1).value);

    this.form.controls.coefficients.at(i - 1).setValue(temporaryCoefficients);
    this.form.controls.constants.at(i - 1).setValue(temporaryConstant);
  }

  // swap equations at index i and i+1, effictively moving equation i down
  moveEquationDown(i: number) {
    if (i === this.equationCount() - 1) return;

    const temporaryCoefficients = this.form.controls.coefficients.at(i).value;
    const temporaryConstant = this.form.controls.constants.at(i).value;

    this.form.controls.coefficients
      .at(i)
      .setValue(this.form.controls.coefficients.at(i + 1).value);
    this.form.controls.constants
      .at(i)
      .setValue(this.form.controls.constants.at(i + 1).value);

    this.form.controls.coefficients.at(i + 1).setValue(temporaryCoefficients);
    this.form.controls.constants.at(i + 1).setValue(temporaryConstant);
  }
}
