module ConfigurationModule
  implicit none

  character(len=20), parameter :: SIMULATION_NAME = "Configuration test";
  logical, parameter :: SIMULATION_OUTPUT = .true.;
  real, parameter :: BOX_WIDTH = 12.0;
  real(kind=8), parameter :: BOX_HEIGHT = 15.0;
  real(kind=16), parameter :: DENSITY = 23.0;
  integer, parameter :: NUM_CELLS = 100;
  integer(kind=8), parameter :: NUM_GROUPS = 2399495729;

end module ConfigurationModule