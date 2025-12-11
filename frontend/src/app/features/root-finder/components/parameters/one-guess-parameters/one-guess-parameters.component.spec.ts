import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OneGuessParametersComponent } from './one-guess-parameters.component';

describe('OneGuessParametersComponent', () => {
  let component: OneGuessParametersComponent;
  let fixture: ComponentFixture<OneGuessParametersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OneGuessParametersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OneGuessParametersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
