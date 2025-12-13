import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IterationStepComponent } from './iteration-step.component';

describe('IterationStepComponent', () => {
  let component: IterationStepComponent;
  let fixture: ComponentFixture<IterationStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IterationStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IterationStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
