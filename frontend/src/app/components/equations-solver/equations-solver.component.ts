import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  inject,
  viewChild,
} from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";
import { EquationsComponent } from "../equations/equations.component";
import { AutoSizeInputDirective } from "ngx-autosize-input";
import { LUParametersComponent } from "../lu-parameters/lu-parameters.component";
import { IterationParametersComponent } from "../iteration-parameters/iteration-parameters.component";
import { JsonPipe } from "@angular/common";

@Component({
  selector: "app-equations-solver",
  imports: [
    ReactiveFormsModule,
    AutoSizeInputDirective,
    EquationsComponent,
    LUParametersComponent,
    IterationParametersComponent,
    JsonPipe,
  ],
  templateUrl: "./equations-solver.component.html",
  styleUrl: "./equations-solver.component.css",
})
export class EquationsSolverComponent {
  private formBuilder = inject(FormBuilder);

  changeDetectorRef = inject(ChangeDetectorRef);

  equationCount = 3;

  methods = [
    { label: "Gauss Elimination", value: "gauss-elimination" },
    { label: "Gauss-Jordan Elimination", value: "gauss-jordan-elimination" },
    { label: "LU Decomposition", value: "lu-decomposition" },
    { label: "Jacobi Iteration", value: "jacobi-iteration" },
    { label: "Gauss-Seidel Iteration", value: "gauss-seidel-iteration" },
  ];

  form = this.formBuilder.group({
    equationCount: [
      this.equationCount.toString(),
      [Validators.required, Validators.pattern(/^[1-9]\d*$/)],
    ],
    equations: [null],
    method: [this.methods[0].value, Validators.required],
    precision: ["", [Validators.pattern(/^[1-9]\d*$/)]],
    parameters: [null],
  });

  parameters = viewChild("parameters", { read: ElementRef });

  ngOnInit() {
    this.form.get("equationCount")?.valueChanges.subscribe((count) => {
      if (this.form.get("equationCount")?.valid) {
        this.equationCount = parseInt(count!, 10);
        this.changeDetectorRef.detectChanges();
      }
    });

    this.form.get("method")?.valueChanges.subscribe(() => {
      this.form.setControl("parameters", this.formBuilder.control(null));
      this.changeDetectorRef.detectChanges();
      setTimeout(() => {
        this.parameters()?.nativeElement.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });
    });
  }

  solve() {
    const value = this.form.value;
    console.log(value);
  }
}
