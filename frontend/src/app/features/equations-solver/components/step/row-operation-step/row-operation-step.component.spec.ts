import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RowOperationStepComponent } from './row-operation-step.component';

describe('RowOperationStepComponent', () => {
  let component: RowOperationStepComponent;
  let fixture: ComponentFixture<RowOperationStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RowOperationStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RowOperationStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
