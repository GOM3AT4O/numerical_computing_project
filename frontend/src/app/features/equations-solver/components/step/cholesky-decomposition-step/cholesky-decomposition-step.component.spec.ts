import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CholeskyDecompositionStepComponent } from './cholesky-decomposition-step.component';

describe('CholeskyDecompositionStepComponent', () => {
  let component: CholeskyDecompositionStepComponent;
  let fixture: ComponentFixture<CholeskyDecompositionStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CholeskyDecompositionStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CholeskyDecompositionStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
