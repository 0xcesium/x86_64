ASM=nasm
LNK=ld

prssr64:
	${ASM} -f elf64 projet-RS_setreuid-x86_64.asm
	${LNK} -m elf_x86_64 projet-RS_setreuid-x86_64.o -o $@

clean:
	rm *.o prssr64
