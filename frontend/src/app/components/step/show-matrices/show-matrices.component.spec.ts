import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowMatricesComponent } from './show-matrices.component';

describe('ShowMatricesComponent', () => {
  let component: ShowMatricesComponent;
  let fixture: ComponentFixture<ShowMatricesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShowMatricesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShowMatricesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
