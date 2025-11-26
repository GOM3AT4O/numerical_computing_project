import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RowOperationComponent } from './row-operation.component';

describe('RowOperationComponent', () => {
  let component: RowOperationComponent;
  let fixture: ComponentFixture<RowOperationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RowOperationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RowOperationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
