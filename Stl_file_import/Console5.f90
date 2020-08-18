!  Console5.f90 
!
!  FUNCTIONS:
!  Console5 - Entry point of console application.
!

!****************************************************************************
!
!  PROGRAM: Console5
!
!  PURPOSE:  Entry point for the console application.
!
!****************************************************************************
    
program test
    implicit none
        real(8) AMATRX(8,8)
        integer i
        do i=1,20
            call UEL(AMATRX)
            call printMatrix(AMATRX)
            print*, ('')
        end do
    end program test

    subroutine UEL (AMATRX)
    !INCLUDE 'ABA_PARAM.INC'
        real(8) AMATRX(8,8), Kij(8,8)

!        C---------- Initialize matrices
        call get_matzero(AMATRX)

!        C---------- Calculate Kij and assemble K matrix
!        C Reading Stiffness Matrix from a txt File
        call Read_Kij(Kij)
        AMATRX=Kij


      end

    subroutine get_matzero(Kij)
    !INCLUDE 'ABA_PARAM.INC'
        real(8) Kij(8,8)
            do i = 1, 8
                do j = 1, 8
                    Kij(i,j)=0.d0
                enddo
            enddo
        
    end
    
    subroutine Read_Kij(Kij)
    !INCLUDE 'ABA_PARAM.INC'
        real(8) Kij(8,8)
        integer c, ilines
    
        open(12, file="C:\\Users\ga53vap\Desktop\Updated_Stl_file_import\Stifness_matrix_Element.txt")
         call get_counter(c)
        if (c==0) then
             read(12,*) ((Kij(i,j), j=1,8), i=1,8)
        else
           
            !call get_counter(c)
            do 50 ilines = (1),(8*c)
             READ(12,*) 
                50  continue 		
    ! read in values
            read(12,*) ((Kij(i,j), j=1,8), i=1,8)
            end if
        
    !call printMatrix(array1,3,3)
    !print*,

    !end do
        close(12)
    end
    
    
    
    subroutine printMatrix(array)
    !INCLUDE 'ABA_PARAM.INC'
    implicit none
        integer i
        real(8) array(8,8)
    

        do i = 1,8
            print*, array(i,:)
        end do
    end 
    
    subroutine get_counter(c)
    integer c, temp
    
        open(10, file="C:\\Users\ga53vap\Desktop\Updated_Stl_file_import\counter.txt")
        read(10,*) c
        close (10,status='delete')
        temp=c+1
        open(10, file="C:\\Users\ga53vap\Desktop\Updated_Stl_file_import\counter.txt",status='new')
        write(10,*) temp
        close (10)
        !write(10,*) temp
        
    end
