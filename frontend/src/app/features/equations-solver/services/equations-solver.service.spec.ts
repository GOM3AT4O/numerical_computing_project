import { TestBed } from '@angular/core/testing';

import { EquationsSolverService } from './equations-solver.service';

describe('EquationsSolverService', () => {
  let service: EquationsSolverService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EquationsSolverService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
