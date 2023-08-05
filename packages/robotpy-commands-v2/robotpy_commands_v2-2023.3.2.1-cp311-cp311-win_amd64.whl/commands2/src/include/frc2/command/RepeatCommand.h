// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#ifdef _WIN32
#pragma warning(push)
#pragma warning(disable : 4521)
#endif

#include <memory>
#include <utility>

#include "frc2/command/CommandBase.h"
#include "frc2/command/CommandHelper.h"

namespace frc2 {
/**
 * A command that runs another command repeatedly, restarting it when it ends,
 * until this command is interrupted. Command instances that are passed to it
 * cannot be added to any other groups, or scheduled individually.
 *
 * <p>The rules for command compositions apply: command instances that are
 * passed to it are owned by the composition and cannot be added to any other
 * composition or scheduled individually, and the composition requires all
 * subsystems its components require.
 *
 * <p>This class is provided by the NewCommands VendorDep
 */
class RepeatCommand : public CommandBase {
 public:
  /**
   * Creates a new RepeatCommand. Will run another command repeatedly,
   * restarting it whenever it ends, until this command is interrupted.
   *
   * @param command the command to run repeatedly
   */
  explicit RepeatCommand(std::shared_ptr<Command> command);

  /**
   * Creates a new RepeatCommand. Will run another command repeatedly,
   * restarting it whenever it ends, until this command is interrupted.
   *
   * @param command the command to run repeatedly
   */
  template <class T, typename = std::enable_if_t<std::is_base_of_v<
                         Command, std::remove_reference_t<T>>>>
  explicit RepeatCommand(T&& command)
      : RepeatCommand(std::make_unique<std::remove_reference_t<T>>(
            std::forward<T>(command))) {}

  RepeatCommand(RepeatCommand&& other) = default;

  // No copy constructors for command groups
  RepeatCommand(const RepeatCommand& other) = delete;

  // Prevent template expansion from emulating copy ctor
  RepeatCommand(RepeatCommand&) = delete;

  void Initialize() override;

  void Execute() override;

  bool IsFinished() override;

  void End(bool interrupted) override;

  bool RunsWhenDisabled() const override;

  Command::InterruptionBehavior GetInterruptionBehavior() const override;

  void InitSendable(wpi::SendableBuilder& builder) override;

 private:
  std::shared_ptr<Command> m_command;
  bool m_ended;
};
}  // namespace frc2

#ifdef _WIN32
#pragma warning(pop)
#endif
