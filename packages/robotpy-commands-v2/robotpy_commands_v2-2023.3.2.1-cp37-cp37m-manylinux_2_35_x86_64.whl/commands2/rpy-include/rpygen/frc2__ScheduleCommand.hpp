
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../src/include/frc2/command/ScheduleCommand.h>

#include <frc2/command/Command.h>
#include <frc2/command/Subsystem.h>
#include <src/helpers.h>



#include <rpygen/frc2__CommandBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename CfgBase>
using PyTrampolineCfgBase_frc2__ScheduleCommand =
    PyTrampolineCfg_frc2__CommandBase<
CfgBase
>;

template <typename CfgBase = EmptyTrampolineCfg>
struct PyTrampolineCfg_frc2__ScheduleCommand :
    PyTrampolineCfgBase_frc2__ScheduleCommand< CfgBase>
{
    using Base = frc2::ScheduleCommand;

    using override_base_Initialize_v = frc2::ScheduleCommand;
    using override_base_IsFinished_v = frc2::ScheduleCommand;
    using override_base_KRunsWhenDisabled_v = frc2::ScheduleCommand;
};


template <typename PyTrampolineBase, typename PyTrampolineCfg>
using PyTrampolineBase_frc2__ScheduleCommand =
    PyTrampoline_frc2__CommandBase<
        PyTrampolineBase
        
        , PyTrampolineCfg
    >
;

template <typename PyTrampolineBase, typename PyTrampolineCfg>
struct PyTrampoline_frc2__ScheduleCommand : PyTrampolineBase_frc2__ScheduleCommand<PyTrampolineBase, PyTrampolineCfg> {
    using PyTrampolineBase_frc2__ScheduleCommand<PyTrampolineBase, PyTrampolineCfg>::PyTrampolineBase_frc2__ScheduleCommand;



#ifndef RPYGEN_DISABLE_Initialize_v
    void Initialize() override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_Initialize_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(void), LookupBase,
            "initialize", );
        return CxxCallBase::Initialize();
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

#ifndef RPYGEN_DISABLE_KRunsWhenDisabled_v
    bool RunsWhenDisabled() const override {
        using LookupBase = typename PyTrampolineCfg::Base;
        using CxxCallBase = typename PyTrampolineCfg::override_base_KRunsWhenDisabled_v;
        PYBIND11_OVERRIDE_IMPL(PYBIND11_TYPE(bool), LookupBase,
            "runsWhenDisabled", );
        return CxxCallBase::RunsWhenDisabled();
    }
#endif




};

}; // namespace rpygen
