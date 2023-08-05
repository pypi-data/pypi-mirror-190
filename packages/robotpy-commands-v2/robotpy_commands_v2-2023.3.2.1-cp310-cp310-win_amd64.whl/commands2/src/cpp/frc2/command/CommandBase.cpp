// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc2/command/CommandBase.h"

#include <wpi/sendable/SendableBuilder.h>
#include <wpi/sendable/SendableRegistry.h>

#include <src/helpers.h>

using namespace frc2;

CommandBase::CommandBase() {
  wpi::SendableRegistry::Add(this, GetTypeName(*this));
}

void CommandBase::AddRequirements(
    std::initializer_list<std::shared_ptr<Subsystem>> requirements) {
  m_requirements.insert(requirements.begin(), requirements.end());
}

void CommandBase::AddRequirements(std::span<std::shared_ptr<Subsystem>> requirements) {
  m_requirements.insert(requirements.begin(), requirements.end());
}

void CommandBase::AddRequirements(wpi::SmallSet<std::shared_ptr<Subsystem>, 4> requirements) {
  m_requirements.insert(requirements.begin(), requirements.end());
}

void CommandBase::AddRequirements(std::shared_ptr<Subsystem> requirement) {
  m_requirements.insert(requirement);
}

wpi::SmallSet<std::shared_ptr<Subsystem>, 4> CommandBase::GetRequirements() const {
  return m_requirements;
}

void CommandBase::SetName(std::string_view name) {
  wpi::SendableRegistry::SetName(this, name);
}

std::string CommandBase::GetName() const {
  return wpi::SendableRegistry::GetName(this);
}

std::string CommandBase::GetSubsystem() const {
  return wpi::SendableRegistry::GetSubsystem(this);
}

void CommandBase::SetSubsystem(std::string_view subsystem) {
  wpi::SendableRegistry::SetSubsystem(this, subsystem);
}

void CommandBase::InitSendable(wpi::SendableBuilder& builder) {
  builder.SetSmartDashboardType("Command");
  builder.AddStringProperty(
      ".name", [this] { return GetName(); }, nullptr);
  builder.AddBooleanProperty(
      "running", [this] { return IsScheduled(); },
      [this](bool value) {
        std::shared_ptr<Command> hack_ptr = convertToSharedPtrHack(this);
        if (!hack_ptr) {
          return;
        }

        bool isScheduled = IsScheduled();
        if (value && !isScheduled) {
          Command_Schedule(hack_ptr);
        } else if (!value && isScheduled) {
          Cancel();
        }
      });
  builder.AddBooleanProperty(
      ".isParented", [this] { return IsComposed(); }, nullptr);
  builder.AddStringProperty(
      "interruptBehavior",
      [this] {
        switch (GetInterruptionBehavior()) {
          case Command::InterruptionBehavior::kCancelIncoming:
            return "kCancelIncoming";
          case Command::InterruptionBehavior::kCancelSelf:
            return "kCancelSelf";
          default:
            return "Invalid";
        }
      },
      nullptr);
  builder.AddBooleanProperty(
      "runsWhenDisabled", [this] { return RunsWhenDisabled(); }, nullptr);
}
