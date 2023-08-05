
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\src\include\frc2\command\ProfiledPIDSubsystem.h>




#include <rpygen/frc2__SubsystemBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename CfgBase>
using PyTrampolineCfgBase_frc2__ProfiledPIDSubsystem =
    PyTrampolineCfg_frc2__SubsystemBase<
CfgBase
>;

template <typename Distance, typename CfgBase = EmptyTrampolineCfg>
struct PyTrampolineCfg_frc2__ProfiledPIDSubsystem :
    PyTrampolineCfgBase_frc2__ProfiledPIDSubsystem< CfgBase>
{
    using Base = frc2::ProfiledPIDSubsystem<Distance>;

    using override_base_Periodic_v = frc2::ProfiledPIDSubsystem<Distance>;
    using override_base_Enable_v = frc2::ProfiledPIDSubsystem<Distance>;
    using override_base_Disable_v = frc2::ProfiledPIDSubsystem<Distance>;
    using override_base_GetMeasurement_v = frc2::ProfiledPIDSubsystem<Distance>;
    using override_base_UseOutput_d_TState = frc2::ProfiledPIDSubsystem<Distance>;
};


template <typename PyTrampolineBase, typename PyTrampolineCfg>
using PyTrampolineBase_frc2__ProfiledPIDSubsystem =
    PyTrampoline_frc2__SubsystemBase<
        PyTrampolineBase
        
        , PyTrampolineCfg
    >
;

template <typename PyTrampolineBase, typename Distance, typename PyTrampolineCfg>
struct PyTrampoline_frc2__ProfiledPIDSubsystem : PyTrampolineBase_frc2__ProfiledPIDSubsystem<PyTrampolineBase, PyTrampolineCfg> {
    using PyTrampolineBase_frc2__ProfiledPIDSubsystem<PyTrampolineBase, PyTrampolineCfg>::PyTrampolineBase_frc2__ProfiledPIDSubsystem;

    using Distance_t = units::unit_t<Distance>;
    using Velocity [[maybe_unused]] = typename frc2::ProfiledPIDSubsystem<Distance>::Velocity;
    using Velocity_t [[maybe_unused]] = typename frc2::ProfiledPIDSubsystem<Distance>::Velocity_t;
    using State [[maybe_unused]] = typename frc2::ProfiledPIDSubsystem<Distance>::State;


#ifndef RPYGEN_DISABLE_Periodic_v
    void Periodic() override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_Periodic_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(void), LookupBase,
            "periodic", );
        return CxxCallBase::Periodic();
    }
#endif

#ifndef RPYGEN_DISABLE_Enable_v
    void Enable() override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_Enable_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(void), LookupBase,
            "enable", );
        return CxxCallBase::Enable();
    }
#endif

#ifndef RPYGEN_DISABLE_Disable_v
    void Disable() override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_Disable_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(void), LookupBase,
            "disable", );
        return CxxCallBase::Disable();
    }
#endif

#ifndef RPYGEN_DISABLE_GetMeasurement_v
    units::unit_t<Distance > GetMeasurement() override {
        using LookupBase = typename PyTrampolineCfg::Base;
        RPYBUILD_OVERRIDE_PURE_NAME(ProfiledPIDSubsystem, PYBIND11_TYPE(units::unit_t<Distance >), LookupBase,
            "_getMeasurement", GetMeasurement, );
    }
#endif

#ifndef RPYGEN_DISABLE_UseOutput_d_TState
    void UseOutput(double output, typename frc::TrapezoidProfile<Distance >::State setpoint) override {
        using LookupBase = typename PyTrampolineCfg::Base;
        RPYBUILD_OVERRIDE_PURE_NAME(ProfiledPIDSubsystem, PYBIND11_TYPE(void), LookupBase,
            "_useOutput", UseOutput, output, setpoint);
    }
#endif



    using frc2::ProfiledPIDSubsystem<Distance>::m_controller;

};

}; // namespace rpygen


namespace rpygen {

using namespace frc2;


template <typename Distance>
struct bind_frc2__ProfiledPIDSubsystem {

        using Distance_t = units::unit_t<Distance>;

        using Velocity [[maybe_unused]] = typename frc2::ProfiledPIDSubsystem<Distance>::Velocity;
    using Velocity_t [[maybe_unused]] = typename frc2::ProfiledPIDSubsystem<Distance>::Velocity_t;
    using State [[maybe_unused]] = typename frc2::ProfiledPIDSubsystem<Distance>::State;

    
      using ProfiledPIDSubsystem_Trampoline = rpygen::PyTrampoline_frc2__ProfiledPIDSubsystem<typename frc2::ProfiledPIDSubsystem<Distance>, Distance, typename rpygen::PyTrampolineCfg_frc2__ProfiledPIDSubsystem<Distance>>;
    static_assert(std::is_abstract<ProfiledPIDSubsystem_Trampoline>::value == false, "frc2::ProfiledPIDSubsystem<Distance> " RPYBUILD_BAD_TRAMPOLINE);
py::class_<typename frc2::ProfiledPIDSubsystem<Distance>, ProfiledPIDSubsystem_Trampoline, frc2::SubsystemBase> cls_ProfiledPIDSubsystem;




    py::module &m;
    std::string clsName;

bind_frc2__ProfiledPIDSubsystem(py::module &m, const char * clsName) :
    cls_ProfiledPIDSubsystem(m, clsName),



    m(m),
    clsName(clsName)
{
    
}

void finish(const char * set_doc = NULL, const char * add_doc = NULL) {

    
  cls_ProfiledPIDSubsystem.doc() =
    "A subsystem that uses a ProfiledPIDController to control an output.  The\n"
"controller is run synchronously from the subsystem's periodic() method.\n"
"\n"
"@see ProfiledPIDController";

  cls_ProfiledPIDSubsystem
      .def(py::init<frc::ProfiledPIDController<Distance >, units::unit_t<Distance >>(),
      py::arg("controller"), py::arg("initialPosition")=Distance_t{ 0}, release_gil(), py::doc(
    "Creates a new ProfiledPIDSubsystem.\n"
"\n"
":param controller:      the ProfiledPIDController to use\n"
":param initialPosition: the initial goal position of the subsystem")
  )
    
      .def("periodic", &frc2::ProfiledPIDSubsystem<Distance>::Periodic, release_gil()
  )
    
      .def("setGoal", static_cast<  void(frc2::ProfiledPIDSubsystem<Distance>::*)(typename frc::TrapezoidProfile<Distance >::State)>(
&frc2::ProfiledPIDSubsystem<Distance>::SetGoal),
      py::arg("goal"), release_gil(), py::doc(
    "Sets the goal state for the subsystem.\n"
"\n"
":param goal: The goal state for the subsystem's motion profile.")
  )
    
      .def("setGoal", static_cast<  void(frc2::ProfiledPIDSubsystem<Distance>::*)(units::unit_t<Distance >)>(
&frc2::ProfiledPIDSubsystem<Distance>::SetGoal),
      py::arg("goal"), release_gil(), py::doc(
    "Sets the goal state for the subsystem.  Goal velocity assumed to be zero.\n"
"\n"
":param goal: The goal position for the subsystem's motion profile.")
  )
    
      .def("enable", &frc2::ProfiledPIDSubsystem<Distance>::Enable, release_gil(), py::doc(
    "Enables the PID control. Resets the controller.")
  )
    
      .def("disable", &frc2::ProfiledPIDSubsystem<Distance>::Disable, release_gil(), py::doc(
    "Disables the PID control.  Sets output to zero.")
  )
    
      .def("isEnabled", &frc2::ProfiledPIDSubsystem<Distance>::IsEnabled, release_gil(), py::doc(
    "Returns whether the controller is enabled.\n"
"\n"
":returns: Whether the controller is enabled.")
  )
    
      .def("getController", &frc2::ProfiledPIDSubsystem<Distance>::GetController, release_gil(), py::doc(
    "Returns the ProfiledPIDController.\n"
"\n"
":returns: The controller.")
  )
    
      .def("_getMeasurement", static_cast<  Distance_t(frc2::ProfiledPIDSubsystem<Distance>::*)()>(&ProfiledPIDSubsystem_Trampoline::GetMeasurement), release_gil(), py::doc(
    "Returns the measurement of the process variable used by the\n"
"ProfiledPIDController.\n"
"\n"
":returns: the measurement of the process variable")
  )
    
      .def("_useOutput", static_cast<  void(frc2::ProfiledPIDSubsystem<Distance>::*)(double, typename frc::TrapezoidProfile<Distance >::State)>(&ProfiledPIDSubsystem_Trampoline::UseOutput),
      py::arg("output"), py::arg("setpoint"), release_gil(), py::doc(
    "Uses the output from the ProfiledPIDController.\n"
"\n"
":param output:   the output of the ProfiledPIDController\n"
":param setpoint: the setpoint state of the ProfiledPIDController, for\n"
"                 feedforward")
  )
    
    .def_readonly("_m_controller", &ProfiledPIDSubsystem_Trampoline::m_controller);

  

    if (set_doc) {
        cls_ProfiledPIDSubsystem.doc() = set_doc;
    }
    if (add_doc) {
        cls_ProfiledPIDSubsystem.doc() = py::cast<std::string>(cls_ProfiledPIDSubsystem.doc()) + add_doc;
    }

    
}

}; // struct bind_frc2__ProfiledPIDSubsystem

}; // namespace rpygen