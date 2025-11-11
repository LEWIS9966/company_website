// 联系表单处理
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const successMessage = document.getElementById('successMessage');

    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // 清除之前的错误信息
            clearErrors();
            
            // 获取表单数据
            const formData = {
                name: document.getElementById('name').value.trim(),
                gender: document.querySelector('input[name="gender"]:checked')?.value,
                phone: document.getElementById('phone').value.trim(),
                email: document.getElementById('email').value.trim(),
                requirements: document.getElementById('requirements').value.trim()
            };

            // 前端验证
            if (!validateForm(formData)) {
                return;
            }

            // 禁用提交按钮
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = '提交中...';

            try {
                // 发送数据到后端
                const response = await fetch('/api/submit-contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (result.success) {
                    // 显示成功消息
                    contactForm.style.display = 'none';
                    successMessage.style.display = 'block';
                    
                    // 滚动到成功消息
                    successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    // 3秒后可以重新显示表单（可选）
                    // setTimeout(() => {
                    //     contactForm.style.display = 'block';
                    //     successMessage.style.display = 'none';
                    //     contactForm.reset();
                    // }, 5000);
                } else {
                    // 显示错误消息
                    showError('submitError', result.message || '提交失败，请稍后重试');
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }
            } catch (error) {
                console.error('Error:', error);
                showError('submitError', '网络错误，请检查网络连接后重试');
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });

        // 实时验证
        const nameInput = document.getElementById('name');
        const phoneInput = document.getElementById('phone');
        const emailInput = document.getElementById('email');
        const requirementsInput = document.getElementById('requirements');

        if (nameInput) {
            nameInput.addEventListener('blur', function() {
                validateField('name', this.value.trim(), '请输入客户称呼');
            });
        }

        if (phoneInput) {
            phoneInput.addEventListener('blur', function() {
                const phone = this.value.trim();
                if (phone) {
                    validatePhone(phone);
                }
            });
        }

        if (emailInput) {
            emailInput.addEventListener('blur', function() {
                const email = this.value.trim();
                if (email) {
                    validateEmail(email);
                }
            });
        }

        if (requirementsInput) {
            requirementsInput.addEventListener('blur', function() {
                validateField('requirements', this.value.trim(), '请填写具体需求');
            });
        }
    }
});

// 表单验证
function validateForm(data) {
    let isValid = true;

    // 验证姓名
    if (!data.name) {
        showError('nameError', '请输入客户称呼');
        isValid = false;
    }

    // 验证性别
    if (!data.gender) {
        showError('genderError', '请选择性别');
        isValid = false;
    }

    // 验证联系方式（至少填写一项）
    if (!data.phone && !data.email) {
        showError('phoneError', '请至少填写手机或邮箱其中一项');
        showError('emailError', '请至少填写手机或邮箱其中一项');
        isValid = false;
    }

    // 验证手机号格式
    if (data.phone && !validatePhone(data.phone)) {
        isValid = false;
    }

    // 验证邮箱格式
    if (data.email && !validateEmail(data.email)) {
        isValid = false;
    }

    // 验证需求
    if (!data.requirements) {
        showError('requirementsError', '请填写具体需求');
        isValid = false;
    }

    return isValid;
}

// 验证单个字段
function validateField(fieldName, value, errorMessage) {
    if (!value) {
        showError(fieldName + 'Error', errorMessage);
        return false;
    } else {
        clearError(fieldName + 'Error');
        return true;
    }
}

// 验证手机号
function validatePhone(phone) {
    const phoneRegex = /^1[3-9]\d{9}$/;
    if (!phoneRegex.test(phone)) {
        showError('phoneError', '手机号格式不正确，请输入11位有效手机号');
        return false;
    } else {
        clearError('phoneError');
        return true;
    }
}

// 验证邮箱
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError('emailError', '邮箱格式不正确');
        return false;
    } else {
        clearError('emailError');
        return true;
    }
}

// 显示错误信息
function showError(errorId, message) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

// 清除错误信息
function clearError(errorId) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

// 清除所有错误信息
function clearErrors() {
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(element => {
        element.textContent = '';
        element.style.display = 'none';
    });
}

