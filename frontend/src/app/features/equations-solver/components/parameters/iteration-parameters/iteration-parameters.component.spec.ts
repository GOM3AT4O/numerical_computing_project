import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IterationParametersComponent } from './iteration-parameters.component';

describe('IterationParametersComponent', () => {
  let component: IterationParametersComponent;
  let fixture: ComponentFixture<IterationParametersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IterationParametersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IterationParametersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
