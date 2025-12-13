import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OneGuessWithMultiplicityParametersComponent } from './one-guess-with-multiplicity-parameters.component';

describe('OneGuessWithMultiplicityParametersComponent', () => {
  let component: OneGuessWithMultiplicityParametersComponent;
  let fixture: ComponentFixture<OneGuessWithMultiplicityParametersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OneGuessWithMultiplicityParametersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OneGuessWithMultiplicityParametersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
