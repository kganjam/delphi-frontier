// Driver-API JIT link of the CDP1 PTX + libcudadevrt, to capture the driver's own error log text.
#include <cstdio>
#include <cuda.h>
int main(int argc, char **argv) {
  char elog[16384] = {0}, ilog[16384] = {0};
  CUdevice dev; CUcontext ctx; CUlinkState ls; void *cubin; size_t sz;
  printf("cuInit %d\n", cuInit(0)); cuDeviceGet(&dev, 0); printf("ctx %d\n", cuCtxCreate(&ctx, 0, dev));
  int maj, min; cuDeviceGetAttribute(&maj, CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR, dev); cuDeviceGetAttribute(&min, CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR, dev);
  printf("compute_capability %d.%d\n", maj, min);
  CUjit_option o[4] = {CU_JIT_ERROR_LOG_BUFFER, CU_JIT_ERROR_LOG_BUFFER_SIZE_BYTES, CU_JIT_INFO_LOG_BUFFER, CU_JIT_INFO_LOG_BUFFER_SIZE_BYTES};
  void *v[4] = {elog, (void *)(size_t)sizeof(elog), ilog, (void *)(size_t)sizeof(ilog)};
  printf("cuLinkCreate %d\n", cuLinkCreate(4, o, v, &ls));
  printf("cuLinkAddFile ptx %d\n", cuLinkAddFile(ls, CU_JIT_INPUT_PTX, argv[1], 0, 0, 0));
  printf("cuLinkAddFile cudadevrt %d\n", cuLinkAddFile(ls, CU_JIT_INPUT_LIBRARY, argv[2], 0, 0, 0));
  printf("cuLinkComplete %d\n", cuLinkComplete(ls, &cubin, &sz));
  printf("ERROR_LOG<<%s>>\nINFO_LOG<<%s>>\n", elog, ilog);
  return 0;
}
