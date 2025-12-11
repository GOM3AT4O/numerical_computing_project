import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TwoGuessesParametersComponent } from './two-guesses-parameters.component';

describe('TwoGuessesParametersComponent', () => {
  let component: TwoGuessesParametersComponent;
  let fixture: ComponentFixture<TwoGuessesParametersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TwoGuessesParametersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TwoGuessesParametersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
