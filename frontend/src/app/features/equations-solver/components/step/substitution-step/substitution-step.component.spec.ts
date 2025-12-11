import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubstitutionStepComponent } from './substitution-step.component';

describe('SubstitutionStepComponent', () => {
  let component: SubstitutionStepComponent;
  let fixture: ComponentFixture<SubstitutionStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubstitutionStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubstitutionStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
