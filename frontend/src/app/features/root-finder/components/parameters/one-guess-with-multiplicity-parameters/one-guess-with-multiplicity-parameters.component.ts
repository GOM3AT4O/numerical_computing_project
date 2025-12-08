import { Component, forwardRef } from "@angular/core";
import {
  ReactiveFormsModule,
  NG_VALUE_ACCESSOR,
  NG_VALIDATORS,
  Validators,
} from "@angular/forms";
import { ParametersComponent } from "../parameters.component";
import { OneGuessWithMultiplicityParameters } from "../../../models/parameters";
import { AutoSizeInputDirective } from "ngx-autosize-input";

@Component({
  selector: "app-one-guess-with-multiplicity-parameters",
  imports: [ReactiveFormsModule, AutoSizeInputDirective],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(
        () => OneGuessWithMultiplicityParametersComponent,
      ),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(
        () => OneGuessWithMultiplicityParametersComponent,
      ),
      multi: true,
    },
  ],
  templateUrl: "./one-guess-with-multiplicity-parameters.component.html",
  styleUrl: "./one-guess-with-multiplicity-parameters.component.css",
})
export class OneGuessWithMultiplicityParametersComponent extends ParametersComponent {
  form = this.formBuilder.group({
    guess: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
    multiplicity: ["", [Validators.required, Validators.pattern(/^[1-9]\d*$/)]],
  });

  override writeValue(value: any): void {
    if (value) {
      if (value.guess) {
        this.form.controls.guess.setValue(value.guess, {
          emitEvent: false,
        });
      }
    }
  }

  override get parameters(): OneGuessWithMultiplicityParameters {
    const value = this.form.value!;

    return {
      guess: value.guess!,
      multiplicity: parseInt(value.multiplicity!, 10),
    };
  }
}
