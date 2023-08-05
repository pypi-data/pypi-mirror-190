
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\src\include\frc2\command\SwerveControllerCommand.h>

#include <frc2/command/Command.h>
#include <frc2/command/Subsystem.h>



#include <rpygen/frc2__CommandBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename CfgBase>
using PyTrampolineCfgBase_frc2__SwerveControllerCommand =
    PyTrampolineCfg_frc2__CommandBase<
CfgBase
>;

template <size_t NumModules, typename CfgBase = EmptyTrampolineCfg>
struct PyTrampolineCfg_frc2__SwerveControllerCommand :
    PyTrampolineCfgBase_frc2__SwerveControllerCommand< CfgBase>
{
    using Base = frc2::SwerveControllerCommand<NumModules>;

    using override_base_Initialize_v = frc2::SwerveControllerCommand<NumModules>;
    using override_base_Execute_v = frc2::SwerveControllerCommand<NumModules>;
    using override_base_End_b = frc2::SwerveControllerCommand<NumModules>;
    using override_base_IsFinished_v = frc2::SwerveControllerCommand<NumModules>;
};


template <typename PyTrampolineBase, typename PyTrampolineCfg>
using PyTrampolineBase_frc2__SwerveControllerCommand =
    PyTrampoline_frc2__CommandBase<
        PyTrampolineBase
        
        , PyTrampolineCfg
    >
;

template <typename PyTrampolineBase, size_t NumModules, typename PyTrampolineCfg>
struct PyTrampoline_frc2__SwerveControllerCommand : PyTrampolineBase_frc2__SwerveControllerCommand<PyTrampolineBase, PyTrampolineCfg> {
    using PyTrampolineBase_frc2__SwerveControllerCommand<PyTrampolineBase, PyTrampolineCfg>::PyTrampolineBase_frc2__SwerveControllerCommand;



#ifndef RPYGEN_DISABLE_Initialize_v
    void Initialize() override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_Initialize_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(void), LookupBase,
            "initialize", );
        return CxxCallBase::Initialize();
    }
#endif

#ifndef RPYGEN_DISABLE_Execute_v
    void Execute() override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_Execute_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(void), LookupBase,
            "execute", );
        return CxxCallBase::Execute();
    }
#endif

#ifndef RPYGEN_DISABLE_End_b
    void End(bool interrupted) override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_End_b;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(void), LookupBase,
            "end", interrupted);
        return CxxCallBase::End(std::move(interrupted));
    }
#endif

#ifndef RPYGEN_DISABLE_IsFinished_v
    bool IsFinished() override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_IsFinished_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(bool), LookupBase,
            "isFinished", );
        return CxxCallBase::IsFinished();
    }
#endif




};

}; // namespace rpygen


namespace rpygen {

using namespace frc2;


template <size_t NumModules>
struct bind_frc2__SwerveControllerCommand {

    
    
    
      using SwerveControllerCommand_Trampoline = rpygen::PyTrampoline_frc2__SwerveControllerCommand<typename frc2::SwerveControllerCommand<NumModules>, NumModules, typename rpygen::PyTrampolineCfg_frc2__SwerveControllerCommand<NumModules>>;
    static_assert(std::is_abstract<SwerveControllerCommand_Trampoline>::value == false, "frc2::SwerveControllerCommand<NumModules> " RPYBUILD_BAD_TRAMPOLINE);
py::class_<typename frc2::SwerveControllerCommand<NumModules>, SwerveControllerCommand_Trampoline, frc2::CommandBase> cls_SwerveControllerCommand;




    py::module &m;
    std::string clsName;

bind_frc2__SwerveControllerCommand(py::module &m, const char * clsName) :
    cls_SwerveControllerCommand(m, clsName),



    m(m),
    clsName(clsName)
{
    
}

void finish(const char * set_doc = NULL, const char * add_doc = NULL) {

    
  cls_SwerveControllerCommand.doc() =
    "A command that uses two PID controllers (PIDController) and a profiled PID\n"
"controller (ProfiledPIDController) to follow a trajectory (Trajectory) with a\n"
"swerve drive.\n"
"\n"
"The command handles trajectory-following, Velocity PID calculations, and\n"
"feedforwards internally. This is intended to be a more-or-less \"complete\n"
"solution\" that can be used by teams without a great deal of controls\n"
"expertise.\n"
"\n"
"Advanced teams seeking more flexibility (for example, those who wish to\n"
"use the onboard PID functionality of a \"smart\" motor controller) may use the\n"
"secondary constructor that omits the PID and feedforward functionality,\n"
"returning only the raw module states from the position PID controllers.\n"
"\n"
"The robot angle controller does not follow the angle given by\n"
"the trajectory but rather goes to the angle given in the final state of the\n"
"trajectory.";

  cls_SwerveControllerCommand
      .def(py::init<frc::Trajectory, std::function<frc::Pose2d ( )>, frc::SwerveDriveKinematics<NumModules >, frc2::PIDController, frc2::PIDController, frc::ProfiledPIDController<units::radians >, std::function<frc::Rotation2d ( )>, std::function<void ( std::array<frc::SwerveModuleState, NumModules> )>, std::span<std::shared_ptr<Subsystem> >>(),
      py::arg("trajectory"), py::arg("pose"), py::arg("kinematics"), py::arg("xController"), py::arg("yController"), py::arg("thetaController"), py::arg("desiredRotation"), py::arg("output"), py::arg("requirements")=std::span<std::shared_ptr<Subsystem> >{}, release_gil(), py::doc(
    "Constructs a new SwerveControllerCommand that when executed will follow the\n"
"provided trajectory. This command will not return output voltages but\n"
"rather raw module states from the position controllers which need to be put\n"
"into a velocity PID.\n"
"\n"
"Note: The controllers will *not* set the outputVolts to zero upon\n"
"completion of the path- this is left to the user, since it is not\n"
"appropriate for paths with nonstationary endstates.\n"
"\n"
":param trajectory:      The trajectory to follow.\n"
":param pose:            A function that supplies the robot pose,\n"
"                        provided by the odometry class.\n"
":param kinematics:      The kinematics for the robot drivetrain.\n"
":param xController:     The Trajectory Tracker PID controller\n"
"                        for the robot's x position.\n"
":param yController:     The Trajectory Tracker PID controller\n"
"                        for the robot's y position.\n"
":param thetaController: The Trajectory Tracker PID controller\n"
"                        for angle for the robot.\n"
":param desiredRotation: The angle that the drivetrain should be\n"
"                        facing. This is sampled at each time step.\n"
":param output:          The raw output module states from the\n"
"                        position controllers.\n"
":param requirements:    The subsystems to require.")
  )
    
      .def(py::init<frc::Trajectory, std::function<frc::Pose2d ( )>, frc::SwerveDriveKinematics<NumModules >, frc2::PIDController, frc2::PIDController, frc::ProfiledPIDController<units::radians >, std::function<void ( std::array<frc::SwerveModuleState, NumModules> )>, std::span<std::shared_ptr<Subsystem> >>(),
      py::arg("trajectory"), py::arg("pose"), py::arg("kinematics"), py::arg("xController"), py::arg("yController"), py::arg("thetaController"), py::arg("output"), py::arg("requirements")=std::span<std::shared_ptr<Subsystem> >{}, release_gil(), py::doc(
    "Constructs a new SwerveControllerCommand that when executed will follow the\n"
"provided trajectory. This command will not return output voltages but\n"
"rather raw module states from the position controllers which need to be put\n"
"into a velocity PID.\n"
"\n"
"Note: The controllers will *not* set the outputVolts to zero upon\n"
"completion of the path- this is left to the user, since it is not\n"
"appropriate for paths with nonstationary endstates.\n"
"\n"
"Note 2: The final rotation of the robot will be set to the rotation of\n"
"the final pose in the trajectory. The robot will not follow the rotations\n"
"from the poses at each timestep. If alternate rotation behavior is desired,\n"
"the other constructor with a supplier for rotation should be used.\n"
"\n"
":param trajectory:      The trajectory to follow.\n"
":param pose:            A function that supplies the robot pose,\n"
"                        provided by the odometry class.\n"
":param kinematics:      The kinematics for the robot drivetrain.\n"
":param xController:     The Trajectory Tracker PID controller\n"
"                        for the robot's x position.\n"
":param yController:     The Trajectory Tracker PID controller\n"
"                        for the robot's y position.\n"
":param thetaController: The Trajectory Tracker PID controller\n"
"                        for angle for the robot.\n"
":param output:          The raw output module states from the\n"
"                        position controllers.\n"
":param requirements:    The subsystems to require.")
  )
    
      .def(py::init<frc::Trajectory, std::function<frc::Pose2d ( )>, frc::SwerveDriveKinematics<NumModules >, frc::HolonomicDriveController, std::function<frc::Rotation2d ( )>, std::function<void ( std::array<frc::SwerveModuleState, NumModules> )>, std::span<std::shared_ptr<Subsystem> >>(),
      py::arg("trajectory"), py::arg("pose"), py::arg("kinematics"), py::arg("controller"), py::arg("desiredRotation"), py::arg("output"), py::arg("requirements")=std::span<std::shared_ptr<Subsystem> >{}, release_gil(), py::doc(
    "Constructs a new SwerveControllerCommand that when executed will follow the\n"
"provided trajectory. This command will not return output voltages but\n"
"rather raw module states from the position controllers which need to be put\n"
"into a velocity PID.\n"
"\n"
"Note: The controllers will *not* set the outputVolts to zero upon\n"
"completion of the path- this is left to the user, since it is not\n"
"appropriate for paths with nonstationary endstates.\n"
"\n"
":param trajectory:      The trajectory to follow.\n"
":param pose:            A function that supplies the robot pose,\n"
"                        provided by the odometry class.\n"
":param kinematics:      The kinematics for the robot drivetrain.\n"
":param controller:      The HolonomicDriveController for the robot.\n"
":param desiredRotation: The angle that the drivetrain should be\n"
"                        facing. This is sampled at each time step.\n"
":param output:          The raw output module states from the\n"
"                        position controllers.\n"
":param requirements:    The subsystems to require.")
  )
    
      .def(py::init<frc::Trajectory, std::function<frc::Pose2d ( )>, frc::SwerveDriveKinematics<NumModules >, frc::HolonomicDriveController, std::function<void ( std::array<frc::SwerveModuleState, NumModules> )>, std::span<std::shared_ptr<Subsystem> >>(),
      py::arg("trajectory"), py::arg("pose"), py::arg("kinematics"), py::arg("controller"), py::arg("output"), py::arg("requirements")=std::span<std::shared_ptr<Subsystem> >{}, release_gil(), py::doc(
    "Constructs a new SwerveControllerCommand that when executed will follow the\n"
"provided trajectory. This command will not return output voltages but\n"
"rather raw module states from the position controllers which need to be put\n"
"into a velocity PID.\n"
"\n"
"Note: The controllers will *not* set the outputVolts to zero upon\n"
"completion of the path- this is left to the user, since it is not\n"
"appropriate for paths with nonstationary endstates.\n"
"\n"
"Note 2: The final rotation of the robot will be set to the rotation of\n"
"the final pose in the trajectory. The robot will not follow the rotations\n"
"from the poses at each timestep. If alternate rotation behavior is desired,\n"
"the other constructor with a supplier for rotation should be used.\n"
"\n"
":param trajectory:   The trajectory to follow.\n"
":param pose:         A function that supplies the robot pose,\n"
"                     provided by the odometry class.\n"
":param kinematics:   The kinematics for the robot drivetrain.\n"
":param controller:   The HolonomicDriveController for the drivetrain.\n"
":param output:       The raw output module states from the\n"
"                     position controllers.\n"
":param requirements: The subsystems to require.")
  )
    
      .def("initialize", &frc2::SwerveControllerCommand<NumModules>::Initialize, release_gil()
  )
    
      .def("execute", &frc2::SwerveControllerCommand<NumModules>::Execute, release_gil()
  )
    
      .def("end", &frc2::SwerveControllerCommand<NumModules>::End,
      py::arg("interrupted"), release_gil()
  )
    
      .def("isFinished", &frc2::SwerveControllerCommand<NumModules>::IsFinished, release_gil()
  )
    
;

  

    if (set_doc) {
        cls_SwerveControllerCommand.doc() = set_doc;
    }
    if (add_doc) {
        cls_SwerveControllerCommand.doc() = py::cast<std::string>(cls_SwerveControllerCommand.doc()) + add_doc;
    }

    
}

}; // struct bind_frc2__SwerveControllerCommand

}; // namespace rpygen