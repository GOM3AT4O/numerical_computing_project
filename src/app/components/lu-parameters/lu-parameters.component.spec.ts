import { ComponentFixture, TestBed } from "@angular/core/testing";

import { LUParametersComponent } from "./lu-parameters.component";

describe("LUParametersComponent", () => {
  let component: LUParametersComponent;
  let fixture: ComponentFixture<LUParametersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LUParametersComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(LUParametersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
