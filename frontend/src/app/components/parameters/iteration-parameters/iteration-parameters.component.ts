import { Component, forwardRef, input } from "@angular/core";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { RangePipe } from "../../../pipes/range.pipe";
import {
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { MatrixComponent } from "../../matrix/matrix.component";
import { ParametersComponent } from "../../parameters/parameters.component";
import { IterationParameters } from "../../../models/parameters";

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

  form = this.formBuilder.group({
    initialGuess: [[] as string[][], Validators.required],
    numberOfIterations: [
      "",
      [Validators.required, Validators.pattern(/^[1-9]\d*$/)],
    ],
    absoluteRelativeError: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
  });

  override get parameters(): IterationParameters {
    const value = this.form.value!;

    return {
      initialGuess: value.initialGuess!.map((value: string[]) =>
        value[0].trim() === "" ? "0" : value[0],
      ),
      numberOfIterations: parseInt(value.numberOfIterations!, 10),
      absoluteRelativeError: value.absoluteRelativeError!,
    };
  }

  writeValue(value: any): void {
    if (value) {
      if (value.initialGuess) {
        this.form
          .get("initialGuess")
          ?.setValue(value.initialGuess, { emitEvent: false });
      }

      if (value.numberOfIterations) {
        this.form
          .get("numberOfIterations")
          ?.setValue(value.numberOfIterations, {
            emitEvent: false,
          });
      }

      if (value.absoluteRelativeError) {
        this.form
          .get("absoluteRelativeError")
          ?.setValue(value.absoluteRelativeError, {
            emitEvent: false,
          });
      }
    }
  }
}
