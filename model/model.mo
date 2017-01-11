package MJC
    import SI = Modelica.SIunits;
    
    // First, a simple model with first order characteristics
    model Motor
        // Motor parameters
        parameter SI.Time T = 0.2;
        parameter Real k = 4.36;
        // State
        SI.AngularVelocity omega;
        // Input
        input SI.Voltage v_in;
        // Output
        SI.Torque tau;
    initial equation
        omega = 0;
    equation
        T * der(omega) = -omega + v_in * k;
        tau = omega / 500;
    end Motor;

    // Base model
    model Robot
        // Include two motors
        Motor motor_l;
        Motor motor_r;

        // Robot parameters
        parameter SI.Length R = 0.07;
        parameter SI.Length L = 0.20;
        parameter SI.Length b = 0.10;
        parameter SI.Mass M = 1.1;
        parameter SI.Inertia J = (M * b^2) / 4;

        // States
        SI.Velocity v;
        SI.AngularVelocity omega;

        // Inputs
        SI.Voltage v_in_left;
        SI.Voltage v_in_right;

        // Kinematic variables
        SI.Position x;
        SI.Position y;
        SI.Angle theta;
    equation
        motor_l.v_in = v_in_left;
        motor_r.v_in = v_in_right;

        M * der(v) = 1/R * (motor_r.tau + motor_r.tau) - v;
        J * der(omega) = L/R * (motor_r.tau - motor_l.tau) - omega;
        // Kinematics
        der(x) = v * cos(theta);
        der(y) = v * sin(theta);
        der(theta) = omega;
    end Robot;

    // Simulation
    model Simulator
        Robot mjc;
    initial equation
        mjc.x = 0;
        mjc.y = 0;
        mjc.theta = 0;
        mjc.v = 0;
        mjc.omega = 0;
    equation
        // Apply inputs -- for now just torque...
        mjc.v_in_left = -1;
        mjc.v_in_right = 1;
    end Simulator;
end MJC;