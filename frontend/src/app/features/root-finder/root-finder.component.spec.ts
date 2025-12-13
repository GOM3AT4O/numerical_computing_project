import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RootFinderComponent } from './root-finder.component';

describe('RootFinderComponent', () => {
  let component: RootFinderComponent;
  let fixture: ComponentFixture<RootFinderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RootFinderComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RootFinderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
