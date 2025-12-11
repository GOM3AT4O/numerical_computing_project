import { Component, forwardRef } from "@angular/core";
import {
  ReactiveFormsModule,
  NG_VALUE_ACCESSOR,
  NG_VALIDATORS,
  Validators,
} from "@angular/forms";
import { ParametersComponent } from "../parameters.component";
import { TwoGuessesParameters } from "../../../models/parameters";
import { AutoSizeInputDirective } from "ngx-autosize-input";

@Component({
  selector: "app-two-guesses-parameters",
  imports: [ReactiveFormsModule, AutoSizeInputDirective],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => TwoGuessesParametersComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => TwoGuessesParametersComponent),
      multi: true,
    },
  ],
  templateUrl: "./two-guesses-parameters.component.html",
  styleUrl: "./two-guesses-parameters.component.css",
})
export class TwoGuessesParametersComponent extends ParametersComponent {
  form = this.formBuilder.group({
    firstGuess: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
    secondGuess: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
  });

  override writeValue(value: any): void {
    if (value) {
      if (value.firstGuess) {
        this.form.controls.firstGuess.setValue(value.firstGuess, {
          emitEvent: false,
        });
      }

      if (value.secondGuess) {
        this.form.controls.secondGuess.setValue(value.secondGuess, {
          emitEvent: false,
        });
      }
    }
  }

  override get parameters(): TwoGuessesParameters {
    const value = this.form.value!;

    return {
      firstGuess: value.firstGuess!,
      secondGuess: value.secondGuess!,
    };
  }
}
