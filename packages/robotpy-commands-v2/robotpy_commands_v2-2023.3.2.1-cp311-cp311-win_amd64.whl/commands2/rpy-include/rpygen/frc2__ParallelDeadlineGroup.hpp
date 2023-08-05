
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\src\include\frc2\command\ParallelDeadlineGroup.h>

#include <frc2/command/Command.h>
#include <frc2/command/Subsystem.h>
#include <src/helpers.h>

#define RPYGEN_DISABLE_Initialize_v
#define RPYGEN_DISABLE_Execute_v
#define RPYGEN_DISABLE_End_b
#define RPYGEN_DISABLE_IsFinished_v
#define RPYGEN_DISABLE_AddCommands_OTshared_ptr_Command__


#include <rpygen/frc2__CommandGroupBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename CfgBase>
using PyTrampolineCfgBase_frc2__ParallelDeadlineGroup =
    PyTrampolineCfg_frc2__CommandGroupBase<
CfgBase
>;

template <typename CfgBase = EmptyTrampolineCfg>
struct PyTrampolineCfg_frc2__ParallelDeadlineGroup :
    PyTrampolineCfgBase_frc2__ParallelDeadlineGroup< CfgBase>
{
    using Base = frc2::ParallelDeadlineGroup;

    using override_base_KRunsWhenDisabled_v = frc2::ParallelDeadlineGroup;
    using override_base_KGetInterruptionBehavior_v = frc2::ParallelDeadlineGroup;
    using override_base_InitSendable_RTSendableBuilder = frc2::ParallelDeadlineGroup;
};


template <typename PyTrampolineBase, typename PyTrampolineCfg>
using PyTrampolineBase_frc2__ParallelDeadlineGroup =
    PyTrampoline_frc2__CommandGroupBase<
        PyTrampolineBase
        
        , PyTrampolineCfg
    >
;

template <typename PyTrampolineBase, typename PyTrampolineCfg>
struct PyTrampoline_frc2__ParallelDeadlineGroup : PyTrampolineBase_frc2__ParallelDeadlineGroup<PyTrampolineBase, PyTrampolineCfg> {
    using PyTrampolineBase_frc2__ParallelDeadlineGroup<PyTrampolineBase, PyTrampolineCfg>::PyTrampolineBase_frc2__ParallelDeadlineGroup;



#ifndef RPYGEN_DISABLE_KRunsWhenDisabled_v
    bool RunsWhenDisabled() const override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_KRunsWhenDisabled_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(bool), LookupBase,
            "runsWhenDisabled", );
        return CxxCallBase::RunsWhenDisabled();
    }
#endif

#ifndef RPYGEN_DISABLE_KGetInterruptionBehavior_v
    Command::InterruptionBehavior GetInterruptionBehavior() const override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_KGetInterruptionBehavior_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(Command::InterruptionBehavior), LookupBase,
            "getInterruptionBehavior", );
        return CxxCallBase::GetInterruptionBehavior();
    }
#endif

#ifndef RPYGEN_DISABLE_InitSendable_RTSendableBuilder
    void InitSendable(wpi::SendableBuilder& builder) override {
        auto custom_fn = [&](py::function fn) {
  auto builderHandle = py::cast(builder, py::return_value_policy::reference);
  fn(builderHandle);
}
;
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_InitSendable_RTSendableBuilder;
        RPYBUILD_OVERRIDE_CUSTOM_IMPL(PYBIND11_TYPE(void), LookupBase,
            "initSendable", InitSendable, builder);
        return CxxCallBase::InitSendable(std::forward<decltype(builder)>(builder));
    }
#endif




};

}; // namespace rpygen
