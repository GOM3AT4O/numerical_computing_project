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
  selector: "app-matrix",
  imports: [ReactiveFormsModule, AutoSizeInputDirective, RangePipe],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => MatrixComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => MatrixComponent),
      multi: true,
    },
  ],
  templateUrl: "./matrix.component.html",
  styleUrl: "./matrix.component.css",
})
export class MatrixComponent
  implements ControlValueAccessor, Validator, OnChanges
{
  private formBuilder = inject(NonNullableFormBuilder);

  rowCount = input<number>(3);
  columnCount = input<number>(3);

  inputs = viewChildren<ElementRef<HTMLInputElement>>("input");

  numberValidator = Validators.pattern(/^[-+]?\d+(\.\d+)?$/);

  form = this.formBuilder.array<FormArray<FormControl<string>>>([]);

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
    if (changes["rowCount"] || changes["columnCount"]) {
      // update the matrix value to match the new dimensions
      this.writeValue(this.form.value);
      this.onChange(this.form.value);
    }
  }

  writeValue(value: any): void {
    // add rows to the matrix until it matches the row count
    while (this.form.length < this.rowCount()) {
      const row = this.formBuilder.array<FormControl<string>>(
        Array.from({ length: this.columnCount() }, () =>
          this.formBuilder.control<string>("", this.numberValidator),
        ),
      );
      this.form.push(row);
    }

    // remove rows from the matrix until it matches the row count
    while (this.form.length > this.rowCount()) {
      this.form.removeAt(this.form.length - 1);
    }

    for (let i = 0; i < this.form.length; i++) {
      const row = this.form.at(i);
      // add columns to the row until it matches the column count
      while (row.length < this.columnCount()) {
        row.push(this.formBuilder.control<string>("", this.numberValidator));
      }

      // remove columns from the row until it matches the column count
      while (row.length > this.columnCount()) {
        row.removeAt(row.length - 1);
      }
    }

    // set the values of the matrix
    for (let i = 0; i < this.rowCount(); i++) {
      for (let j = 0; j < this.columnCount(); j++) {
        this.form
          .at(i)
          .at(j)
          .setValue(value?.[i]?.[j] ?? "");
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
    return this.form.valid ? null : { matrixInvalid: true };
  }

  onKeyDown(i: number, j: number, event: KeyboardEvent) {
    const input = this.inputs()[i * this.columnCount() + j].nativeElement;

    // navigate inputs based on arrow key pressed, if possible
    switch (event.key) {
      case "ArrowUp":
        i = i > 0 ? i - 1 : i;
        break;
      case "ArrowDown":
        i = i + 1 < this.rowCount() ? i + 1 : i;
        break;
      case "ArrowLeft":
        if (input.value.length !== 0 && input.selectionStart !== 0) {
          return;
        }
        j = j > 0 ? j - 1 : j;
        break;
      case "ArrowRight":
        if (
          input.value.length !== 0 &&
          input.selectionStart !== input.value.length
        ) {
          return;
        }
        j = j + 1 < this.columnCount() ? j + 1 : j;
        break;
      default:
        return;
    }

    event.preventDefault();
    // set focus to the new input
    this.inputs()[i * this.columnCount() + j].nativeElement.focus();
  }
}
