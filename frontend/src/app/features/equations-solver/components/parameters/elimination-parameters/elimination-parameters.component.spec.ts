import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EliminationParametersComponent } from './elimination-parameters.component';

describe('EliminationParametersComponent', () => {
  let component: EliminationParametersComponent;
  let fixture: ComponentFixture<EliminationParametersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EliminationParametersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EliminationParametersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
