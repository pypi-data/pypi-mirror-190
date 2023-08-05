// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc2/command/button/NetworkButton.h"

#include <wpi/deprecated.h>

using namespace frc2;

WPI_IGNORE_DEPRECATED
NetworkButton::NetworkButton(nt::BooleanTopic topic)
    : NetworkButton(topic.Subscribe(false)) {}

NetworkButton::NetworkButton(nt::BooleanSubscriber sub)
    : Button([sub = std::make_shared<nt::BooleanSubscriber>(std::move(sub))] {
        return sub->GetTopic().GetInstance().IsConnected() && sub->Get();
      }) {}
WPI_UNIGNORE_DEPRECATED

NetworkButton::NetworkButton(std::shared_ptr<nt::NetworkTable> table,
                             std::string_view field)
    : NetworkButton(table->GetBooleanTopic(field)) {}

NetworkButton::NetworkButton(std::string_view table, std::string_view field)
    : NetworkButton(nt::NetworkTableInstance::GetDefault(), table, field) {}

NetworkButton::NetworkButton(nt::NetworkTableInstance inst,
                             std::string_view table, std::string_view field)
    : NetworkButton(inst.GetTable(table), field) {}
