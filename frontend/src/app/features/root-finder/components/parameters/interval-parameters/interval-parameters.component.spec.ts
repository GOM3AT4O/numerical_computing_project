import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IntervalParametersComponent } from './interval-parameters.component';

describe('IntervalParametersComponent', () => {
  let component: IntervalParametersComponent;
  let fixture: ComponentFixture<IntervalParametersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IntervalParametersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IntervalParametersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
