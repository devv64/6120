#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"
#include <random>

using namespace llvm;

namespace {

struct RandomizePass : public PassInfoMixin<RandomizePass> {
    PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM) {
      std::random_device rd;
      std::mt19937 gen(rd());
      std::uniform_int_distribution<> dis(0, 3);
      
      for (auto &F : M) {
        std::vector<BinaryOperator*> randomizeOps;
        for (auto &B : F) {
          for (auto &I : B) {
            if(auto *BO = dyn_cast<BinaryOperator>(&I)) {
              auto opcode = BO->getOpcode();
              if (opcode == Instruction::Add ||
                  opcode == Instruction::Sub ||
                  opcode == Instruction::Mul ||
                  opcode == Instruction::SDiv) {
                randomizeOps.push_back(BO);
              }
            }
          }
        }
        
        for (auto *BO : randomizeOps) {
          IRBuilder<> builder(BO);
          Value* lhs = BO->getOperand(0);
          Value* rhs = BO->getOperand(1);
          
          std::string oldOpName = BO->getOpcodeName();
          
          int rnd = dis(gen);
          Value* newOp = nullptr;
          std::string newOpName;
          
          switch (rnd) {
            case 0:
              newOp = builder.CreateAdd(lhs, rhs);
              newOpName = "add";
              break;
            case 1:
              newOp = builder.CreateSub(lhs, rhs);
              newOpName = "sub";
              break;
            case 2:
              newOp = builder.CreateMul(lhs, rhs);
              newOpName = "mul";
              break;
            case 3:
              newOp = builder.CreateSDiv(lhs, rhs);
              newOpName = "sdiv";
              break;
          }
          
          errs() << "Changing " << oldOpName << " to " << newOpName << "\n";
          errs() << "New operation: " << *newOp << "\n";
          
          for (auto &U : BO->uses()) {
            User* user = U.getUser();
            errs() << "Updating use in: " << *user << "\n";
            user->setOperand(U.getOperandNo(), newOp);
          }
        }
      }
      
      return PreservedAnalyses::none();
    };
};
}
extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
    return {
        .APIVersion = LLVM_PLUGIN_API_VERSION,
        .PluginName = "Randomize pass",
        .PluginVersion = "v0.1",
        .RegisterPassBuilderCallbacks = [](PassBuilder &PB) {
            PB.registerPipelineStartEPCallback(
                [](ModulePassManager &MPM, OptimizationLevel Level) {
                    MPM.addPass(RandomizePass());
                });
        }
    };
}