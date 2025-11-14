import { ComponentFixture, TestBed } from "@angular/core/testing";

import { EquationsSolverComponent } from "./equations-solver.component";

describe("EquationsSolverComponent", () => {
  let component: EquationsSolverComponent;
  let fixture: ComponentFixture<EquationsSolverComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EquationsSolverComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(EquationsSolverComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
