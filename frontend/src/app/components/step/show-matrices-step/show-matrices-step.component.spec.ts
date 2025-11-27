import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowMatricesStepComponent } from './show-matrices-step.component';

describe('ShowMatricesStepComponent', () => {
  let component: ShowMatricesStepComponent;
  let fixture: ComponentFixture<ShowMatricesStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShowMatricesStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShowMatricesStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
