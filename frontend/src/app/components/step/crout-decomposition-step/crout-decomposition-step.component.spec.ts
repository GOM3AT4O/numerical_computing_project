import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CroutDecompositionStepComponent } from './crout-decomposition-step.component';

describe('CroutDecompositionStepComponent', () => {
  let component: CroutDecompositionStepComponent;
  let fixture: ComponentFixture<CroutDecompositionStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CroutDecompositionStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CroutDecompositionStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
